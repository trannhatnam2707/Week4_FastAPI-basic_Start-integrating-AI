import React, { useState, useEffect } from 'react';
import { Link, useNavigate , useParams } from 'react-router-dom';
import { Card, Button, Modal, Input, message, Space } from 'antd';
import axios from 'axios';


const { TextArea } = Input;

const PostDetail = () => {

  const {id} = useParams()
  const navigate = useNavigate();
  const [post, setPost] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isEditModalVisible, setIsEditModalVisible] = useState(false);
  const [editForm, setEditForm] = useState({
    title: post?.title || '',
    content: post?.content || '',
    author: post?.author || ''  
  });

  useEffect(() => {
    const fetchPost = async() => {
      try {
        const res = await axios.get(`http://localhost:8000/posts/${id}`)
        setPost(res.data.post) // lấy theo API trả về
        setLoading(false)
      }
      catch (error)
      {
        message.error("không tìm thấy bài viết hoặc Lỗi server")
        setLoading(false)
      }
    };
    fetchPost();
  }, [id]);

  const handleDelete = async () => {
    try {
      await axios.delete(`http://localhost:8000/posts/${post.id}`);
      message.success('Đã xóa bài viết thành công');
      navigate('/');
    } catch (err) {
      message.error('Không thể xóa bài viết');
    }
  };

      // Refresh data
      const handleUpdate = async () => {
        try {
          await axios.put(`http://localhost:8000/posts/${post.id}`, editForm);
          message.success('Cập nhật bài viết thành công');
          setIsEditModalVisible(false);
          navigate('/'); // về Home → PostList fetch lại
        } catch (err) {
          message.error('Không thể cập nhật bài viết');
        }
      };
      

  const showEditModal = () => {
    setEditForm({
      title: post.title,
      content: post.content,
      author: post.author
    });
    setIsEditModalVisible(true);
  };

  if(loading) {
    return <div style={{padding:"20px"}}>Đang tải dữ liệu</div>
  }

  if (!post) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <h2>Không tìm thấy bài viết</h2>
        <Link to="/">
          <Button type="primary">Quay lại trang chủ</Button>
        </Link>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px' }}>
      <Card 
        title={<span style={{fontSize: 24, fontWeight: 600}}>Chi tiết bài viết</span>}
        extra={
          <Space>
            <Button type="primary" onClick={showEditModal}>
              Cập nhật
            </Button>
            <Button danger onClick={handleDelete}>
              Xóa
            </Button>
            <Link to="/">
              <Button>Quay lại</Button>
            </Link>
          </Space>
        }
      >
        <h2 style={{fontSize: 28, marginBottom: 16}}>{post.title}</h2>
        <p style={{fontSize: 16, lineHeight: 1.6, marginBottom: 16}}>{post.content}</p>
        <p style={{fontSize: 14, color: '#666'}}>
          <strong>Tác giả:</strong> {post.author}
        </p>
        <p style={{fontSize: 14, color: '#666'}}>
          <strong>ID:</strong> {post.id}
        </p>
      </Card>

      {/* Modal cập nhật */}
      <Modal
        title="Cập nhật bài viết"
        open={isEditModalVisible}
        onOk={handleUpdate}
        onCancel={() => setIsEditModalVisible(false)}
        okText="Cập nhật"
        cancelText="Hủy"
        width={600}
      >
        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', marginBottom: 8, fontWeight: 600 }}>Tiêu đề:</label>
          <Input
            value={editForm.title}
            onChange={(e) => setEditForm({...editForm, title: e.target.value})}
            placeholder="Nhập tiêu đề"
          />
        </div>
        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', marginBottom: 8, fontWeight: 600 }}>Nội dung:</label>
          <TextArea
            value={editForm.content}
            onChange={(e) => setEditForm({...editForm, content: e.target.value})}
            placeholder="Nhập nội dung"
            rows={6}
          />
        </div>
        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', marginBottom: 8, fontWeight: 600 }}>Tác giả:</label>
          <Input
            value={editForm.author}
            onChange={(e) => setEditForm({...editForm, author: e.target.value})}
            placeholder="Nhập tên tác giả"
          />
        </div>
      </Modal>
    </div>
  );
};

export default PostDetail;
