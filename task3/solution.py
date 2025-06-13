def convert_list_to_intervals(timestemps: list) -> list:
    print("Конвертируем список интервалов в пары")
    pair_list = []
    for i in range(0, len(timestemps), 2):
        pair_list.append((timestemps[i], timestemps[i + 1]))
    return pair_list

def limit_intervals_to_the_lesson(start_lesson: int, end_lesson: int, list_of_intervals: list) -> list:
    print("Ограничиваем интервалы участников началом и концом урока")
    intervals_within_a_lesson = []
    for member_time_online in list_of_intervals:
        start_member_online = member_time_online[0]
        end_member_online = member_time_online[1]
        start = max(start_member_online, start_lesson)
        end = min(end_member_online, end_lesson)
        if start < end:
            intervals_within_a_lesson.append((start, end))

    return intervals_within_a_lesson

def count_intersections(pupil_interval_list: list, tutor_interval_list: list) -> list:
    print("Считаем количество пересечений ученика и учителя")
    intersections_list = []
    for pupil_interval in pupil_interval_list:
        for tutor_interval in tutor_interval_list:
            start = max(pupil_interval[0], tutor_interval[0])
            end = min(pupil_interval[1], tutor_interval[1])
            if start < end:
                intersections_list.append((start, end))

    if not intersections_list:
        return []

    sorted_intersections_list = sorted(intersections_list)
    finish_intersections_list = [sorted_intersections_list[0]]

    for current in sorted_intersections_list[1:]:
        last = finish_intersections_list[-1]
        if current[0] <= last[1]:
            finish_intersections_list[-1] = (last[0], max(last[1], current[1]))
        else:
            finish_intersections_list.append(current)

    return finish_intersections_list



def appearance(intervals: dict[str, list[int]]) -> int:
    pupil_pair_list = convert_list_to_intervals(intervals['pupil'])
    tutor_pair_list = convert_list_to_intervals(intervals['tutor'])

    limited_to_lesson_pupil_list = limit_intervals_to_the_lesson(intervals['lesson'][0], intervals['lesson'][1], pupil_pair_list)
    limited_to_lesson_tutor_list = limit_intervals_to_the_lesson(intervals['lesson'][0], intervals['lesson'][1], tutor_pair_list)

    intersections_list = count_intersections(limited_to_lesson_pupil_list, limited_to_lesson_tutor_list)
    seconds_list = []
    for interval in intersections_list:
        seconds_list.append(interval[1] - interval[0])

    return sum(seconds_list)
    



tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['intervals'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
