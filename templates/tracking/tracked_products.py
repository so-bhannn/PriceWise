{% extends "pricewise/home.html" %}
{% block content %}

<h1>Tracked Products</h1>
{% if products %}
<tr>
    <th>Product</th>
    <th>Price</th>
    {% for product in products %}
    <td>{{ product.name }}</td>
    <td>${{ product.current_price }}</td>
    <td>
        <a href="{{ product.url }}" target="_blank">View</a>
        {% if product in tracked_products %}
        <span>Tracked</span>
        {% else %}
        <a href="{% url 'track_product' product.id %}">Track</a>
        {% endif %}
    </td>
    {% endfor %}
</tr>
{% endif %}
{% endblock content %}