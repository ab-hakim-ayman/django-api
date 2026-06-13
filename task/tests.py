import json

from django.test import Client, TestCase
from django.urls import reverse

from task.models import Task


class TaskApiTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.list_url = reverse("task-list")

    def test_create_task(self):
        response = self.client.post(
            self.list_url,
            data=json.dumps(
                {
                    "title": "Write docs",
                    "description": "Add README endpoint section",
                    "is_completed": False,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(response.json()["title"], "Write docs")

    def test_list_tasks(self):
        task = Task.objects.create(title="Ship feature", description="Push branch")

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["tasks"]), 1)
        self.assertEqual(response.json()["tasks"][0]["id"], task.id)

    def test_retrieve_task(self):
        task = Task.objects.create(title="Review PR", description="Check CI")

        response = self.client.get(reverse("task-detail", args=[task.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], task.title)

    def test_update_task(self):
        task = Task.objects.create(title="Old title", description="Before update")

        response = self.client.patch(
            reverse("task-detail", args=[task.id]),
            data=json.dumps({"title": "New title", "is_completed": True}),
            content_type="application/json",
        )

        task.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(task.title, "New title")
        self.assertTrue(task.is_completed)

    def test_delete_task(self):
        task = Task.objects.create(title="Delete me")

        response = self.client.delete(reverse("task-detail", args=[task.id]))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(pk=task.id).exists())

    def test_create_task_requires_title(self):
        response = self.client.post(
            self.list_url,
            data=json.dumps({"description": "Missing title"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
