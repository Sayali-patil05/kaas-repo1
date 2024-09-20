from datetime import datetime


def calculate_streak(logins: list[datetime]) -> tuple[int, int]:
    left = 0
    right = 1

    current_streak = 0
    longest_streak = 0

    while right < len(logins):
        diff = (
            logins[right] - logins[left]
        ).days  # difference between the 2 login time
        if (
            diff == 1
        ):  # if the differnce between 2 consecutive logins is 1 day then we have a steak
            current_streak += 1  # increment to keep track of the current streak
        else:
            # the difference is no longer 1 streak broke, now check if this is longest streak
            longest_streak = max(current_streak, longest_streak)

        right += 1  # increment make sure it isn't an infinte loop
        left += 1

    longest_streak = max(
        current_streak, longest_streak
    )  # if the current streak is the longest
    return (current_streak, longest_streak)
