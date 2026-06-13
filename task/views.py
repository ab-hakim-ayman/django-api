import json

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from task.models import Task


def _serialize_task(task: Task) -> dict[str, object]:
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_completed": task.is_completed,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }


def _parse_json(
    request: HttpRequest,
) -> tuple[dict[str, object] | None, JsonResponse | None]:
    try:
        raw_body = request.body.decode("utf-8") or "{}"
        return json.loads(raw_body), None
    except json.JSONDecodeError:
        return None, JsonResponse({"error": "Invalid JSON payload."}, status=400)


def _validate_title(data: dict[str, object]) -> str | None:
    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return None
    return title.strip()


def _validate_is_completed(value: object) -> bool | None:
    if isinstance(value, bool):
        return value
    return None


@csrf_exempt
def task_collection(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        tasks = [_serialize_task(task) for task in Task.objects.all()]
        return JsonResponse({"tasks": tasks})

    if request.method == "POST":
        data, error_response = _parse_json(request)
        if error_response:
            return error_response

        assert data is not None
        title = _validate_title(data)
        if not title:
            return JsonResponse({"error": "The 'title' field is required."}, status=400)

        description = data.get("description", "")
        is_completed = _validate_is_completed(data.get("is_completed", False))
        if is_completed is None:
            return JsonResponse(
                {"error": "The 'is_completed' field must be a boolean."},
                status=400,
            )
        task = Task.objects.create(
            title=title,
            description=description if isinstance(description, str) else "",
            is_completed=is_completed,
        )
        return JsonResponse(_serialize_task(task), status=201)

    return JsonResponse({"error": "Method not allowed."}, status=405)


@csrf_exempt
def task_resource(request: HttpRequest, task_id: int) -> JsonResponse:
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(_serialize_task(task))

    if request.method in {"PUT", "PATCH"}:
        data, error_response = _parse_json(request)
        if error_response:
            return error_response

        assert data is not None
        if "title" in data:
            title = _validate_title(data)
            if not title:
                return JsonResponse(
                    {"error": "The 'title' field must be a non-empty string."},
                    status=400,
                )
            task.title = title

        if "description" in data:
            description = data["description"]
            if not isinstance(description, str):
                return JsonResponse(
                    {"error": "The 'description' field must be a string."},
                    status=400,
                )
            task.description = description

        if "is_completed" in data:
            is_completed = _validate_is_completed(data["is_completed"])
            if is_completed is None:
                return JsonResponse(
                    {"error": "The 'is_completed' field must be a boolean."},
                    status=400,
                )
            task.is_completed = is_completed

        task.save()
        return JsonResponse(_serialize_task(task))

    if request.method == "DELETE":
        task.delete()
        return JsonResponse({}, status=204)

    return JsonResponse({"error": "Method not allowed."}, status=405)
