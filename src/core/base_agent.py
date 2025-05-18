from dataclasses import dataclass
import chainlit as cl

@dataclass
class JobItem:
    title: str
    description: str

class AgentAI:
    def __init__(self, jobs: list[JobItem]):
        self.task_list = cl.TaskList()
        self.task_list.status = "Running..."
        self.tasks = []
        self.jobs=jobs


    async def init_tasks(self):
        for i in self.jobs:
            task = cl.Task(i.__dict__["title"], status=cl.TaskStatus.READY)
            self.tasks.append(task)
            await self.task_list.add_task(task)
    

    async def start(self, action):
        await self.init_tasks()

        # Start process tasks
        for index in range(len(self.tasks)):
            self.tasks[index].staus = cl.TaskStatus.RUNNING
            await self.task_list.send()

            # Process custom action on agents
            await action(self.jobs[index])

            self.tasks[index].staus = cl.TaskStatus.DONE
            await self.task_list.send()

        self.task_list.status = "Done"
        await self.task_list.send()