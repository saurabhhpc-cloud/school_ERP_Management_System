class SchoolScopedAdmin:
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, "userprofile") and request.user.userprofile.school:
            return qs.filter(school=request.user.userprofile.school)
        return qs.none()

    def save_model(self, request, obj, form, change):
        if not obj.pk and hasattr(request.user, "userprofile"):
            obj.school = request.user.userprofile.school
        super().save_model(request, obj, form, change)
