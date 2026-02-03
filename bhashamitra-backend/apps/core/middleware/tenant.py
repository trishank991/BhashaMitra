"""Tenant middleware for multi-tenant support.

This middleware resolves the tenant from the request and attaches it
to the request object for downstream use.

For now, defaults to the single 'PeppiAcademy' tenant.
In the future, this can resolve tenants from subdomains or headers.
"""
from django.utils.deprecation import MiddlewareMixin


class TenantMiddleware(MiddlewareMixin):
    """Resolve tenant from request and attach to request object."""

    def process_request(self, request):
        # For now, set tenant to None (single-tenant mode)
        # In the future, resolve from subdomain: request.get_host().split('.')[0]
        # Or from header: request.META.get('HTTP_X_TENANT_SLUG')
        request.tenant = None

        # If the user is authenticated and has a tenant, use that
        if hasattr(request, 'user') and request.user.is_authenticated:
            if hasattr(request.user, 'tenant') and request.user.tenant:
                request.tenant = request.user.tenant
