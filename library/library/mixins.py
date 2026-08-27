from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Allow access only to staff members."""

    def test_func(self):
        return self.request.user.is_staff
