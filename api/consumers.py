from channels.generic.websocket import AsyncJsonWebsocketConsumer

class TaskConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.project_slug = self.scope['url_route']["kwargs"]["project_slug"]
        self.group_name = f'project_{self.project_slug}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def task_update(self, event):
        await self.send_json(event["data"])

    async def comment_update(self,event):
        await self.send_json(event["data"])    
        

        