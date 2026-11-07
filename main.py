import tkinter as tk
from controllers.phong_may_controller import PhongMayController
from models.phong_may_model import PhongMayModel
from views.phong_may_view import PhongMayView


def main() -> None:
    """Điểm khởi chạy chính của ứng dụng theo mô hình MVC."""
    root = tk.Tk()
    model = PhongMayModel()
    view = PhongMayView(root)
    _controller = PhongMayController(model=model, view=view)
    root.mainloop()


if __name__ == "__main__":
    main()
