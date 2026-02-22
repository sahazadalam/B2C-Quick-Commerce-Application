import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String userServiceUrl = 'http://localhost:8001';
  static const String productServiceUrl = 'http://localhost:8002';
  static const String cartOrderServiceUrl = 'http://localhost:8003';
  static const String deliveryServiceUrl = 'http://localhost:8004';

  Future<Map<String, String>> _getHeaders() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('token');
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  // Auth APIs
  Future<Map<String, dynamic>> register(
      String name, String email, String password) async {
    final response = await http.post(
      Uri.parse('$userServiceUrl/register'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'name': name,
        'email': email,
        'password': password,
      }),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception(json.decode(response.body)['detail']);
    }
  }

  Future<String> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$userServiceUrl/login'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'email': email,
        'password': password,
      }),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      final token = data['access_token'];
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('token', token);
      return token;
    } else {
      throw Exception(json.decode(response.body)['detail']);
    }
  }

  // Product APIs
  Future<List<dynamic>> getCategories() async {
    final response = await http.get(
      Uri.parse('$productServiceUrl/categories'),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load categories');
    }
  }

  Future<List<dynamic>> getProducts({String? category}) async {
    String url = '$productServiceUrl/products';
    if (category != null) {
      url += '?category=$category';
    }

    final response = await http.get(Uri.parse(url));

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load products');
    }
  }

  Future<Map<String, dynamic>> getProduct(String productId) async {
    final response = await http.get(
      Uri.parse('$productServiceUrl/products/$productId'),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load product');
    }
  }

  // Cart APIs
  Future<void> addToCart(String userId, String productId, int quantity) async {
    final headers = await _getHeaders();
    final response = await http.post(
      Uri.parse('$cartOrderServiceUrl/cart/add?user_id=$userId'),
      headers: headers,
      body: json.encode({
        'product_id': productId,
        'quantity': quantity,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to add to cart');
    }
  }

  Future<Map<String, dynamic>> getCart(String userId) async {
    final headers = await _getHeaders();
    final response = await http.get(
      Uri.parse('$cartOrderServiceUrl/cart?user_id=$userId'),
      headers: headers,
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load cart');
    }
  }

  Future<void> removeFromCart(String userId, String productId) async {
    final headers = await _getHeaders();
    final response = await http.post(
      Uri.parse(
          '$cartOrderServiceUrl/cart/remove?user_id=$userId&product_id=$productId'),
      headers: headers,
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to remove from cart');
    }
  }

  // Order APIs
  Future<Map<String, dynamic>> createOrder(
      String userId, List<Map<String, dynamic>> items, double total) async {
    final headers = await _getHeaders();
    final response = await http.post(
      Uri.parse('$cartOrderServiceUrl/order/create'),
      headers: headers,
      body: json.encode({
        'user_id': userId,
        'items': items,
        'total': total,
      }),
    );

    if (response.statusCode == 200) {
      final orderData = json.decode(response.body);
      // Initiate delivery tracking
      await initiateDelivery(orderData['order_id']);
      return orderData;
    } else {
      throw Exception('Failed to create order');
    }
  }

  Future<List<dynamic>> getOrders(String userId) async {
    final headers = await _getHeaders();
    final response = await http.get(
      Uri.parse('$cartOrderServiceUrl/orders?user_id=$userId'),
      headers: headers,
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load orders');
    }
  }

  // Delivery APIs
  Future<void> initiateDelivery(String orderId) async {
    final headers = await _getHeaders();
    await http.post(
      Uri.parse('$deliveryServiceUrl/order/$orderId/initiate'),
      headers: headers,
    );
  }

  Future<Map<String, dynamic>> getOrderStatus(String orderId) async {
    final headers = await _getHeaders();
    final response = await http.get(
      Uri.parse('$deliveryServiceUrl/order/$orderId/status'),
      headers: headers,
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to get order status');
    }
  }
}
