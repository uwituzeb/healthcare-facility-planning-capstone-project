import { useState, useEffect } from 'react';

const AdminDashboard = () => {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      const response = await fetch('/api/getSignupRequests');
      const data = await response.json();
      setRequests(data);
    } catch (error) {
      console.error('Error fetching requests:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (requestId) => {
    try {
      const response = await fetch('/api/approveUser', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ requestId })
      });

      if (response.ok) {
        alert('User approved successfully!');
        fetchRequests();
      }
    } catch (error) {
      alert('Error approving user');
    }
  };

  const handleReject = async (requestId) => {
    try {
      const response = await fetch('/api/rejectUser', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ requestId })
      });

      if (response.ok) {
        alert('User rejected');
        fetchRequests();
      }
    } catch (error) {
      alert('Error rejecting user');
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Pending Signup Requests</h1>
      <div className="space-y-4">
        {requests.filter(r => r.status === 'pending').map((request) => (
          <div key={request.id} className="border p-4 rounded-lg">
            <p><strong>Name:</strong> {request.first_name} {request.last_name}</p>
            <p><strong>Email:</strong> {request.email}</p>
            <p><strong>Role:</strong> {request.role}</p>
            <p><strong>Requested:</strong> {new Date(request.created_at).toLocaleDateString()}</p>
            <div className="mt-4 space-x-2">
              <button
                onClick={() => handleApprove(request.id)}
                className="bg-green-500 text-white px-4 py-2 rounded"
              >
                Approve
              </button>
              <button
                onClick={() => handleReject(request.id)}
                className="bg-red-500 text-white px-4 py-2 rounded"
              >
                Reject
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdminDashboard;