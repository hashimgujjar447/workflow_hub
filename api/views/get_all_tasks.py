from rest_framework.views import APIView
from rest_framework.response import Response
from tasks.models import Task
from api.serializers.task_serializers import DashboardTaskSerializer

class DashboardTasksView(APIView):
    

    def get(self, request):
        user = request.user

        # Base queryset (secure)
        base_qs = Task.objects.filter(
            project__workspace__members__user=user
        ).select_related('project', 'project__workspace').distinct()

        # Recent Tasks (latest 5)
        recent_tasks = base_qs.order_by('-created_at')[:5]

        # My Tasks (assigned to user, 5)
        my_tasks = base_qs.filter(
            assigned_to__member=user
        ).order_by('-created_at')[:5]

        return Response({
            "recent_tasks": DashboardTaskSerializer(recent_tasks, many=True).data,
            "my_tasks": DashboardTaskSerializer(my_tasks, many=True).data,
        })