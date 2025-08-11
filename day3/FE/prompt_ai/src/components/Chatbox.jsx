import React, { useEffect, useRef } from 'react'
import { List, Spin } from 'antd';
import Message from './Message'


const Chatbox = ({message, loading}) => {

    // // ref trỏ tới phần tử cuối danh sách tin nhắn
    const messageEndRef = useRef(null)

    useEffect(() => {
      // cuộn xuống cuối khi có tin nhắn mới hoặc loading thay đổi
      messageEndRef.current?.scrollIntoView({behavior:"smooth"});
    },[message,loading]);


  return (
    <div style ={{
      flex: 1,
      overflowY: "auto",
      background:"#fff",
      padding:"10px",
      borderRadius:"8px",
      border:"1px solid #f0f0f0"
    }}>
      <List
       dataSource={message}
       renderItem={(msg) => (
        <List.Item>
           <Message sender={msg.sender} text={msg.text}/>
        </List.Item>
       )}
      />
        {loading && (
          <div style={{textAlign: "center", padding:"10px"}}>
              <Spin tip = "AI đang trả lời ..."/>
          </div>
        )}
          <div ref={messageEndRef}/> 
    </div>
  )
}

export default Chatbox
