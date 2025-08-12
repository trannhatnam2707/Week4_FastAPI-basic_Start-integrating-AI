import React, { useState, useEffect} from 'react'
import axios from "axios"
import {Button, Card, Input, List, message} from "antd"
import { Link } from 'react-router-dom'



  const {Search, TextArea } = Input
  const PostList = () => {

  const [posts, setPosts] = useState([])
  const [title, setTitle] = useState("")
  const [content, setContent] = useState("")
  const [author, setAuthor] = useState("")
  const [search, Setsearch] = useState("")

  const fetchPosts = async () => {
    try {
      const res = await axios.get("http://localhost:8000/posts");
      setPosts([...res.data.posts].reverse());
    } catch (err) {
      message.error("Lỗi khi tải bài viết");
    }
  };

  const handlePost = async () => {
    if (!title || !content || !author) {
      message.warning("Nhập đầy đủ tiêu đề, nội dung và tác giả");
      return;
    }
    try {
      await axios.post("http://localhost:8000/posts", {
        title,
        content,
        author,
      });
        message.success({
        content: 'Đăng bài thành công',
        duration: 2,
        style: { marginTop: '50px' },
        });

      setTitle("");
      setContent("");
      setAuthor("");
      fetchPosts();
    } catch (err) {
      message.error("Không thể đăng bài")
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  //Lọc posts theo điều kiện: title chứa chuỗi search (không phân biệt hoa/thường).
  const filteredPosts = posts.filter((post) =>
    post?.title?.toLowerCase().includes(search.toLowerCase())
  );


  return (
    <div style={{ padding: '20px', height: "100vh", display:"flex", flexDirection:"column"}}>
      <Search
          placeholder='Tim bài viết ...'
          allowClear
          value={search}
          onChange={(e) => Setsearch(e.target.value)}
          onSearch={(value) => Setsearch(value)}
          style={{marginBottom: '20px'}}
      />
      <div style={{display:"flex", flex:1, gap:"20px"}}>
        {/*danh sách bài viết - sidebar*/}
          <div style={{flex: '0 0 320px', maxWidth: 320, height: 'calc(100vh - 100px)', overflowY:"auto", borderRight: '1px solid #f0f0f0', paddingRight: 8}}>
            <List
              header={<b> Bài viết gần đây </b>}
              // Lấy danh sách bài post đã lọc theo điều kiện
              dataSource={filteredPosts}
              renderItem={(item) => (
                <List.Item>
                  <Card size="small" style={{width:"100%"}}>
                    <div style={{display:'flex', flexDirection:'column'}}>
                      <span style={{fontWeight:600}}>{item?.title}</span>
                      <small style={{color:'#888'}}>Tác giả: {item.author}</small>
                      <Link to={`/PostDetail/${item.id}`} style={{marginTop: 6}}>Xem chi tiết</Link>
                    </div>
                  </Card>
                </List.Item>
              )}
            />
          </div>
          {/* Form đăng bài */}
          <div style={{flex:4}}>
              <Card 
                title={<span style={{fontSize: 18, fontWeight: 600}}>Bài đăng mới</span>}
                style={{height: '100%'}}
              >
                  <Input
                    size="large"
                    placeholder='Title'
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    style={{marginBottom:"12px"}}
                  />
                  <TextArea
                    size='large'
                    placeholder='Content'
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    rows={10}
                    style={{ 
                      marginBottom: "12px", 
                      fontSize: 16,
                      minHeight: 400,
                      resize: 'vertical'
                    }}
                  />
                  <Input 
                    size="large"
                    placeholder='Author'
                    value={author}
                    onChange={(e) => setAuthor(e.target.value)}
                    style={{marginBottom:"12px"}}
                  />
                  <Button type="primary" size="large" onClick={handlePost}>
                    Post
                  </Button>
              </Card>
          </div>
      </div>
    </div>
  )
}

export default PostList
