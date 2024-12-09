from django.shortcuts import render
from .models import Property

def property_listing(request):
    # Initial query set to show all properties
    properties = Property.objects.all()

    # Filter based on user selections
    # Filtering based on price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)

    # Filtering based on location
    location_filter = request.GET.getlist('location')
    if location_filter:
        properties = properties.filter(location__in=location_filter)

    # Filtering based on property type
    type_filter = request.GET.getlist('type')
    if type_filter:
        properties = properties.filter(type__in=type_filter)

    # Filtering based on property status
    status_filter = request.GET.getlist('status')
    if status_filter:
        properties = properties.filter(status__in=status_filter)

    # Collect all unique values for the filters (for the dropdowns)
    locations = Property.objects.values_list('location', flat=True).distinct()
    property_types = Property.objects.values_list('type', flat=True).distinct()
    statuses = Property.objects.values_list('status', flat=True).distinct()

    # Pass the filtered properties and filter options to the template
    context = {
        'properties': properties,
        'locations': locations,
        'property_types': property_types,
        'statuses': statuses,
        'selected_location': location_filter,
        'selected_type': type_filter,
        'selected_status': status_filter,
        'min_price': min_price,
        'max_price': max_price,
    }

    return render(request, 'property_app/property_listing.html', context)
