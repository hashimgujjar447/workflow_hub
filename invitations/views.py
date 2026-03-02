from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from workspaces.models import Workspace,WorkspaceMember
from .forms import WorkspaceInviteForm
from django.core.exceptions import PermissionDenied
from .models import WorkspaceInvite
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings



@login_required
def send_invite(request, slug):
    workspace = get_object_or_404(Workspace, slug=slug)

    # Permission check
    if not WorkspaceMember.objects.filter(
        workspace=workspace,
        user=request.user,
        role='manager'
    ).exists():
        raise PermissionDenied

    if request.method == "POST":
        email = request.POST.get("email")
        role = request.POST.get("role")

        # 1️⃣ Basic validation
        if not email:
            return render(request, "invitations/send_invite.html", {
                "workspace": workspace,
                "error": "Email is required."
            })

        # 2️⃣ Prevent inviting existing member
        if WorkspaceMember.objects.filter(
            workspace=workspace,
            user__email=email
        ).exists():
            return render(request, "invitations/send_invite.html", {
                "workspace": workspace,
                "error": "User is already a member."
            })

        # 3️⃣ Prevent duplicate pending invite
        if WorkspaceInvite.objects.filter(
            workspace=workspace,
            email=email,
            status="pending"
        ).exists():
            return render(request, "invitations/send_invite.html", {
                "workspace": workspace,
                "error": "Invite already sent."
            })

        # 4️⃣ Create invite
        invite=WorkspaceInvite.objects.create(
            workspace=workspace,
            invited_by=request.user,
            email=email,
            role=role
        )
        invite_link = request.build_absolute_uri(
            reverse("all_invites")
        )

        send_mail(
            subject=f"You are invited to join {workspace.name}",
            message=f"""
        Hi,

        You have been invited to join {workspace.name}.

        Click below to visit invites:
        {invite_link}

        This link expires in 7 days.
        """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,)

        return redirect("workspace_detail", slug=slug)

    return render(request, "invitations/send_invite.html", {
        "workspace": workspace
    })

@login_required
def get_invites(request):
    invites = WorkspaceInvite.objects.filter(
        email=request.user.email,
        status="pending"
    )

    if request.method == "POST":
        action = request.POST.get("action")
        token = request.POST.get("token")

        invite = get_object_or_404(
            WorkspaceInvite,
            token=token,
            status="pending"
        )

        # 🔒 Security check
        if invite.email.lower() != request.user.email.lower():
            raise PermissionDenied("This invite is not for you.")

        if invite.is_expired():
            invite.status = "expired"
            invite.save()
            raise PermissionDenied("Invite expired.")

        if action == "accept":
            WorkspaceMember.objects.get_or_create(
                workspace=invite.workspace,
                user=request.user,
                defaults={"role": invite.role}
            )

            invite.status = "accepted"
            invite.save()

        elif action == "reject":
            invite.status = "rejected"
            invite.save()

        return redirect("workspaces")

    return render(request, 'invitations/all_invites.html', {
        'invites': invites
    })