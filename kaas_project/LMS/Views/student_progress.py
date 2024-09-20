from ..models import Material, Course, ViewRecord


def calculate_progress(user, course: Course) -> float:
    count_materials = Material.objects.filter(course=course.course_id).count()
    # print(f"{count_materials=}")
    if count_materials == 0:
        return 0.0  # You cannot make progress unless there are materials in the course
    viewed_material = set(
        map(
            lambda x: x.material.material_id,
            ViewRecord.objects.filter(user=user, course=course.course_id).all(),
        )
    )
    # print(f"{viewed_material=}")
    distinct_materials_viewed = len(viewed_material)
    # print(f"{distinct_materials_viewed=}")
    return distinct_materials_viewed / count_materials
