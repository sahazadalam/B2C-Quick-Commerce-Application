import 'package:flutter/material.dart';
import '../services/api_service.dart';

class OrderTrackingScreen extends StatefulWidget {
  final String orderId;

  OrderTrackingScreen({required this.orderId});

  @override
  _OrderTrackingScreenState createState() => _OrderTrackingScreenState();
}

class _OrderTrackingScreenState extends State<OrderTrackingScreen> {
  final ApiService _apiService = ApiService();
  Map<String, dynamic>? _deliveryStatus;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadDeliveryStatus();
  }

  Future<void> _loadDeliveryStatus() async {
    try {
      final status = await _apiService.getOrderStatus(widget.orderId);
      setState(() {
        _deliveryStatus = status;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to load delivery status: $e')),
      );
    }
  }

  int _getStatusIndex(String status) {
    switch (status) {
      case 'PLACED':
        return 0;
      case 'PACKED':
        return 1;
      case 'OUT_FOR_DELIVERY':
        return 2;
      case 'DELIVERED':
        return 3;
      default:
        return 0;
    }
  }

  String _getStatusMessage(String status) {
    switch (status) {
      case 'PLACED':
        return 'Your order has been placed';
      case 'PACKED':
        return 'Your order has been packed';
      case 'OUT_FOR_DELIVERY':
        return 'Your order is out for delivery';
      case 'DELIVERED':
        return 'Your order has been delivered';
      default:
        return status;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Track Order'),
        backgroundColor: Colors.green,
        foregroundColor: Colors.white,
      ),
      body: _isLoading
          ? Center(child: CircularProgressIndicator())
          : _deliveryStatus == null
              ? Center(
                  child: Text('No delivery information found'),
                )
              : Padding(
                  padding: EdgeInsets.all(24.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Order ID: ${widget.orderId}',
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.grey[600],
                        ),
                      ),
                      SizedBox(height: 8),
                      Text(
                        'Current Status:',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      SizedBox(height: 8),
                      Container(
                        padding: EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: Colors.green.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: Colors.green),
                        ),
                        child: Row(
                          children: [
                            Icon(
                              Icons.info_outline,
                              color: Colors.green,
                            ),
                            SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                _getStatusMessage(_deliveryStatus!['status']),
                                style: TextStyle(
                                  fontSize: 16,
                                  color: Colors.green,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      SizedBox(height: 32),
                      Text(
                        'Delivery Progress:',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      SizedBox(height: 24),
                      // Stepper for delivery status
                      Column(
                        children: [
                          _buildStatusStep(
                            'Order Placed',
                            'Your order has been confirmed',
                            0,
                            _getStatusIndex(_deliveryStatus!['status']),
                          ),
                          _buildStatusStep(
                            'Order Packed',
                            'Your items have been packed',
                            1,
                            _getStatusIndex(_deliveryStatus!['status']),
                          ),
                          _buildStatusStep(
                            'Out for Delivery',
                            'Delivery partner is on the way',
                            2,
                            _getStatusIndex(_deliveryStatus!['status']),
                          ),
                          _buildStatusStep(
                            'Delivered',
                            'Order delivered successfully',
                            3,
                            _getStatusIndex(_deliveryStatus!['status']),
                          ),
                        ],
                      ),
                      SizedBox(height: 32),
                      Text(
                        'Last Updated:',
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.grey[600],
                        ),
                      ),
                      SizedBox(height: 4),
                      Text(
                        _deliveryStatus!['last_updated'],
                        style: TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                ),
    );
  }

  Widget _buildStatusStep(
      String title, String subtitle, int step, int currentStep) {
    bool isCompleted = step < currentStep;
    bool isCurrent = step == currentStep;

    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Column(
          children: [
            Container(
              width: 30,
              height: 30,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color:
                    isCompleted || isCurrent ? Colors.green : Colors.grey[300],
              ),
              child: Center(
                child: isCompleted
                    ? Icon(Icons.check, color: Colors.white, size: 16)
                    : Text(
                        '${step + 1}',
                        style: TextStyle(
                          color: isCurrent ? Colors.white : Colors.grey[600],
                          fontWeight: FontWeight.bold,
                        ),
                      ),
              ),
            ),
            if (step < 3)
              Container(
                width: 2,
                height: 40,
                color: step < currentStep ? Colors.green : Colors.grey[300],
              ),
          ],
        ),
        SizedBox(width: 12),
        Expanded(
          child: Padding(
            padding: EdgeInsets.only(bottom: step < 3 ? 24 : 0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: isCurrent ? FontWeight.bold : FontWeight.normal,
                    color:
                        isCompleted || isCurrent ? Colors.black : Colors.grey,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  subtitle,
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
