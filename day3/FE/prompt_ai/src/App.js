import { useState } from 'react';
import './App.css';
import axios  from 'axios';
import { Layout, Typography } from 'antd';
import Chatbox from './components/Chatbox';
import ChatInput from './components/ChatInput';

function App() {
  const  {Header, Content, Footer} = Layout
  const {Title} = Typography 
  const [messages, setMessages] = useState('')

  const [loading, setLoading] = useState(false)

  const sendMessage = async (text) => {
      setMessages((prev) => [...prev, {sender:"user",text}]);
      setLoading(true);

      try{
        const res = await axios.post("http://127.0.0.1:8000/ask", {prompt: text});
        const AIReply = res.data.reply;
        setMessages((prev) => [...prev, {sender:"AI", text:AIReply}]);
      }
      catch (err) { 
        setMessages((prev) =>
         [...prev, {sender:"AI", text:" Lỗi khi gọi API"}]
        );
      }
      finally{
        setLoading(false)
      }};
      

  return (
    <Layout style={{height: "100vh"}}>
        <Header style={{ background:"#170e0eff", display:"flex", alignItems:"center"}}>
          <Title level={3} style={{color:"#fff", margin: 0}}>
            ChatBox 
          </Title>
        </Header>

        <Content style={{padding:"20px", display:"flex", flexDirection:"column"}}>
          <Chatbox message={messages} loading={loading}/>
        </Content>

        <Footer>
            <ChatInput onSend={sendMessage}/>
        </Footer>
    </Layout>
  );
}

export default App;
