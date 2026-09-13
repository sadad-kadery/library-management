def role_flags(request):
    user = request.user
    if not user.is_authenticated:
        return {}
    return {
        'is_reception_user': user.is_superuser or user.groups.filter(name='Reception').exists(),
        'is_manager_user': user.is_superuser or user.groups.filter(name='Manager').exists(),
    }