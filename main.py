from datetime import datetime, timedelta


def transform_intervals(intervals: list[dict[str, str]]) -> list(dict[datetime, datetime]):
    transformed_intervals = [
        {
            'start': datetime.strptime(interval['start'], "%H:%M"),
            'stop': datetime.strptime(interval['stop'], "%H:%M")
        }
        for interval in intervals
    ]
    return sorted(
        transformed_intervals,
        key=lambda x: x["start"]
    )

        
def calculate_free_windows(
    start_time: datetime,
    end_time: datetime,
    busy_intervals: list[dict[str, str]],
    window_duration: timedelta
) -> list[dict[datetime, datetime]]:
    free_windows = []
    busy_intervals = transform_intervals(busy_intervals)
    
    current_time = start_time
    while current_time < end_time - window_duration:
        busy_flag = False
        for interval in busy_intervals:
            if interval['start'] <= current_time < interval['stop']:
                busy_flag = True
                current_time = interval['stop']
                break
        if not busy_flag:
            stop_time = current_time + window_duration
            free_windows.append(
                {
                    'start': current_time,
                    'stop': stop_time
                }
            )
            current_time += window_duration
    return free_windows

    
def main() -> None:
    start_time = datetime.strptime("09:00", "%H:%M")
    end_time = datetime.strptime("21:00", "%H:%M")
    busy_intervals = [
        {'start': '10:30', 'stop': '10:50'},
        {'start': '18:40', 'stop': '18:50'},
        {'start': '14:40', 'stop': '15:50'},
        {'start': '16:40', 'stop': '17:20'},
        {'start': '20:05', 'stop': '20:20'}
    ]
    window_duration = timedelta(minutes=30)
    
    free_windows = calculate_free_windows(
        start_time,
        end_time,
        busy_intervals,
        window_duration
    )
    for window in free_windows:
        print(f"Свободное окно: {window['start'].strftime('%H:%M')} - {window['stop'].strftime('%H:%M')}")


if __name__ == "__main__":
    main()
