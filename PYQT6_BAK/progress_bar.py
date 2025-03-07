import asyncio
from PyQt6.QtWidgets import QProgressBar, QStatusBar


async def update_progress_bar(progress_bar: QProgressBar):
    try:
        for i in range(10000):
            progress_bar.setValue(i + 1)
            await asyncio.sleep(0.001)
    except Exception as e:
        print(f"Exception:{e}")


def run_now_process_bar(status_bar: QStatusBar):
    progress_bar = QProgressBar()
    status_bar.addWidget(progress_bar)
    progress_bar.setMaximum(10000)
    asyncio.run(update_progress_bar(progress_bar))
    status_bar.removeWidget(progress_bar)
