from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

from workspaces.models import Workspace, WorkspaceMember
from invitations.models import WorkspaceInvite
from api.serializers.invitations import WorkspaceInviteSerializer


# 🔥 1. SEND INVITE (CreateAPIView)
class SendInviteView(generics.CreateAPIView):
    serializer_class = WorkspaceInviteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        slug = self.kwargs.get("slug")
        workspace = get_object_or_404(Workspace, slug=slug)

        # ✅ Permission check
        if not WorkspaceMember.objects.filter(
            workspace=workspace,
            user=request.user,
            role__in=['owner', 'manager']
        ).exists():
            return Response({"error": "Permission denied"}, status=403)

        email = request.data.get("email")
        role = request.data.get("role", "member")

        if not email:
            return Response({"error": "Email is required"}, status=400)

        # ✅ Already member check
        if WorkspaceMember.objects.filter(
            workspace=workspace,
            user__email=email
        ).exists():
            return Response({"error": "User already a member"}, status=400)

        # ✅ Duplicate invite check
        if WorkspaceInvite.objects.filter(
            workspace=workspace,
            email=email,
            status="pending"
        ).exists():
            return Response({"error": "Invite already sent"}, status=400)

        # ✅ Create invite
        invite = WorkspaceInvite.objects.create(
            workspace=workspace,
            invited_by=request.user,
            email=email,
            role=role
        )

        invite_link = f"http://localhost:3000/invites/{invite.token}"

        send_mail(
            subject=f"You are invited to join {workspace.name}",
            message=f"Click to join: {invite_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"message": "Invite sent successfully"}, status=201)


# 🔥 2. LIST USER INVITES (ListAPIView)
class ListInvitesView(generics.ListAPIView):
    serializer_class = WorkspaceInviteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkspaceInvite.objects.filter(
            email=self.request.user.email,
            status="pending"
        ).order_by('-created_at')


# 🔥 3. ACCEPT / REJECT INVITE (APIView style inside Generic)
class HandleInviteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.data.get("token")
        action = request.data.get("action")

        invite = get_object_or_404(
            WorkspaceInvite,
            token=token,
            status="pending"
        )

        # 🔒 Security check
        if invite.email.lower() != request.user.email.lower():
            return Response({"error": "Not your invite"}, status=403)

        # ⏳ Expiry check
        if invite.is_expired():
            invite.status = "expired"
            invite.save()
            return Response({"error": "Invite expired"}, status=400)

        if action == "accept":
            WorkspaceMember.objects.get_or_create(
                workspace=invite.workspace,
                user=request.user,
                defaults={"role": invite.role}
            )
            invite.status = "accepted"

        elif action == "reject":
            invite.status = "rejected"

        else:
            return Response({"error": "Invalid action"}, status=400)

        invite.save()

        return Response({"message": f"Invite {action}ed successfully"})