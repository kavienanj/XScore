"""
This module is used to handle exam start, end and several functions,
create a single object TimedExam() and handle it.
"""

from datetime import datetime


class TimedExam:

    def __init__(self):
        self.status = False
        self.exam = None
        self.start = None
        self.over = None

    @property
    def duration(self):
        if self.exam is not None:
            return self.exam.duration
        return None

    def set_exam(self, exam):
        self.exam = exam

    def cleaned_start(self):
        if self.start is not None:
            return self.start.strftime("%H:%M:%S")
        return None

    def cleaned_over(self):
        if self.over is not None:
            return self.over.strftime("%H:%M:%S")
        return None

    def activate(self):
        self.exam.active = True
        self.exam.save()
        self.status = True
        self.start = datetime.now()
        print(f"""
        ======= EXAM {self.exam} STARTED AT {self.start} ======
        """)
        self.over = self.start + self.duration

    def reset(self):
        print(f"""
        ======= EXAM {self.exam} FINISHED AT {self.over} ======
        """)
        self.exam.active = False
        self.exam.save()
        self.__init__()
