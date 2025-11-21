'use client';

import { useState, useEffect } from 'react';
import { X, Plus, Trash2, UserPlus, PackagePlus } from 'lucide-react';

export default function CreateOrderModal({ isOpen, onClose, onSave }) {
  const [formData, setFormData] = useState({
    customer_id: '',
    status: 'pending',
    payment_method: 'Credit Card',
    notes: '',
    order_items: [{ product_id: '', quantity: 1, unit_price: 0 }]
  });
  const [customers, setCustomers] = useState([]);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Quick add modals
  const [showQuickAddCustomer, setShowQuickAddCustomer] = useState(false);
  const [showQuickAddProduct, setShowQuickAddProduct] = useState(false);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '', phone: '', address: '' });
  const [newProduct, setNewProduct] = useState({ name: '', category: '', price: 0, stock: 0, description: '' });

  useEffect(() => {
    if (isOpen) {
      fetchCustomersAndProducts();
    }
  }, [isOpen]);

  const fetchCustomersAndProducts = async () => {
    try {
      const token = localStorage.getItem('access_token');
      
      const [customersRes, productsRes] = await Promise.all([
        fetch('http://localhost:8000/api/customers', {
          headers: { 'Authorization': `Bearer ${token}` }
        }),
        fetch('http://localhost:8000/api/products', {
          headers: { 'Authorization': `Bearer ${token}` }
        })
      ]);

      if (customersRes.ok) {
        const customersData = await customersRes.json();
        setCustomers(customersData);
      }

      if (productsRes.ok) {
        const productsData = await productsRes.json();
        setProducts(productsData);
      }
    } catch (err) {
      console.error('Error fetching data:', err);
    }
  };

  const handleQuickAddCustomer = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/customers', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newCustomer)
      });

      if (response.ok) {
        const createdCustomer = await response.json();
        setCustomers([...customers, createdCustomer]);
        setFormData({ ...formData, customer_id: createdCustomer.id });
        setNewCustomer({ name: '', email: '', phone: '', address: '' });
        setShowQuickAddCustomer(false);
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'Failed to create customer');
      }
    } catch (err) {
      alert('Error creating customer');
    }
  };

  const handleQuickAddProduct = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/products', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newProduct)
      });

      if (response.ok) {
        const createdProduct = await response.json();
        setProducts([...products, createdProduct]);
        setNewProduct({ name: '', category: '', price: 0, stock: 0, description: '' });
        setShowQuickAddProduct(false);
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'Failed to create product');
      }
    } catch (err) {
      alert('Error creating product');
    }
  };

  const handleAddItem = () => {
    setFormData({
      ...formData,
      order_items: [...formData.order_items, { product_id: '', quantity: 1, unit_price: 0 }]
    });
  };

  const handleRemoveItem = (index) => {
    const newItems = formData.order_items.filter((_, i) => i !== index);
    setFormData({ ...formData, order_items: newItems });
  };

  const handleItemChange = (index, field, value) => {
    const newItems = [...formData.order_items];
    newItems[index][field] = value;

    if (field === 'product_id' && value) {
      const product = products.find(p => p.id === parseInt(value));
      if (product) {
        newItems[index].unit_price = product.price;
      }
    }

    setFormData({ ...formData, order_items: newItems });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (!formData.customer_id) {
      setError('Please select or create a customer');
      setLoading(false);
      return;
    }

    if (formData.order_items.some(item => !item.product_id || item.quantity < 1)) {
      setError('Please fill all order items correctly');
      setLoading(false);
      return;
    }

    try {
      const token = localStorage.getItem('access_token');
      
      const payload = {
        customer_id: parseInt(formData.customer_id),
        status: formData.status,
        payment_method: formData.payment_method,
        notes: formData.notes || null,
        order_items: formData.order_items.map(item => ({
          product_id: parseInt(item.product_id),
          quantity: parseInt(item.quantity),
          unit_price: parseFloat(item.unit_price)
        }))
      };

      const response = await fetch('http://localhost:8000/api/orders', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        onSave();
        handleClose();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to create order');
      }
    } catch (err) {
      setError('Network error creating order');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setFormData({
      customer_id: '',
      status: 'pending',
      payment_method: 'Credit Card',
      notes: '',
      order_items: [{ product_id: '', quantity: 1, unit_price: 0 }]
    });
    setError('');
    setShowQuickAddCustomer(false);
    setShowQuickAddProduct(false);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-white/30 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 sticky top-0 bg-white z-10">
          <h2 className="text-2xl font-bold text-gray-900">Create New Order</h2>
          <button onClick={handleClose} className="text-gray-400 hover:text-gray-600">
            <X className="w-6 h-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          {/* Customer Selection with Quick Add */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="block text-sm font-medium text-gray-700">Customer *</label>
              <button
                type="button"
                onClick={() => setShowQuickAddCustomer(!showQuickAddCustomer)}
                className="flex items-center gap-1 px-3 py-1 text-sm bg-green-600 text-white rounded hover:bg-green-700"
              >
                <UserPlus className="w-4 h-4" />
                New Customer
              </button>
            </div>

            {showQuickAddCustomer ? (
              <div className="p-4 bg-blue-50 rounded-lg space-y-3">
                <input
                  type="text"
                  placeholder="Customer Name *"
                  value={newCustomer.name}
                  onChange={(e) => setNewCustomer({ ...newCustomer, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  required
                />
                <input
                  type="email"
                  placeholder="Email *"
                  value={newCustomer.email}
                  onChange={(e) => setNewCustomer({ ...newCustomer, email: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  required
                />
                <input
                  type="text"
                  placeholder="Phone"
                  value={newCustomer.phone}
                  onChange={(e) => setNewCustomer({ ...newCustomer, phone: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
                <input
                  type="text"
                  placeholder="Address"
                  value={newCustomer.address}
                  onChange={(e) => setNewCustomer({ ...newCustomer, address: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={handleQuickAddCustomer}
                    className="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                  >
                    Add Customer
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowQuickAddCustomer(false)}
                    className="px-4 py-2 bg-gray-300 rounded-lg hover:bg-gray-400"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <select
                value={formData.customer_id}
                onChange={(e) => setFormData({ ...formData, customer_id: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="">Select a customer</option>
                {customers.map((customer) => (
                  <option key={customer.id} value={customer.id}>
                    {customer.name} - {customer.email}
                  </option>
                ))}
              </select>
            )}
          </div>

          {/* Order Items - Manual Entry */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <label className="block text-sm font-medium text-gray-700">Order Items *</label>
              <button
                type="button"
                onClick={handleAddItem}
                className="flex items-center gap-1 px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                <Plus className="w-4 h-4" />
                Add Item
              </button>
            </div>

            <div className="space-y-3">
              {formData.order_items.map((item, index) => (
                <div key={index} className="flex gap-2 p-3 bg-gray-50 rounded-lg">
                  <select
                    value={item.product_id}
                    onChange={(e) => handleItemChange(index, 'product_id', e.target.value)}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    required
                  >
                    <option value="">Select product</option>
                    {products.map((product) => (
                      <option key={product.id} value={product.id}>
                        {product.name} - ${product.price}
                      </option>
                    ))}
                  </select>

                  <input
                    type="number"
                    min="1"
                    value={item.quantity}
                    onChange={(e) => handleItemChange(index, 'quantity', e.target.value)}
                    className="w-20 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="Qty"
                    required
                  />

                  <input
                    type="number"
                    step="0.01"
                    value={item.unit_price}
                    onChange={(e) => handleItemChange(index, 'unit_price', e.target.value)}
                    className="w-28 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    placeholder="Price"
                    required
                  />

                  {formData.order_items.length > 1 && (
                    <button
                      type="button"
                      onClick={() => handleRemoveItem(index)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Status and Payment */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
              <select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              >
                <option value="pending">Pending</option>
                <option value="processing">Processing</option>
                <option value="completed">Completed</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Payment Method</label>
              <select
                value={formData.payment_method}
                onChange={(e) => setFormData({ ...formData, payment_method: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              >
                <option value="Credit Card">Credit Card</option>
                <option value="PayPal">PayPal</option>
                <option value="Bank Transfer">Bank Transfer</option>
                <option value="Cash">Cash</option>
              </select>
            </div>
          </div>

          {/* Notes */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Notes</label>
            <textarea
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
              rows={3}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              placeholder="Add any notes..."
            />
          </div>

          {/* Actions */}
          <div className="flex gap-3 pt-4 border-t">
            <button
              type="button"
              onClick={handleClose}
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 font-medium"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium disabled:opacity-50"
              disabled={loading}
            >
              {loading ? 'Creating...' : 'Create Order'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}