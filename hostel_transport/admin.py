from django.contrib import admin
from .models import Hostel, HostelRoom, HostelAllocation, TransportRoute, TransportAssignment

admin.site.register(Hostel)
admin.site.register(HostelRoom)
admin.site.register(HostelAllocation)
admin.site.register(TransportRoute)
admin.site.register(TransportAssignment)