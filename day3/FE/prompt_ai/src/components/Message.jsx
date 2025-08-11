import React from 'react'
import { Avatar, Card, Typography } from 'antd';
import {RobotOutlined , UserOutlined}  from "@ant-design/icons";

const { Text }= Typography;

const Message = ({sender, text}) => {

  const isUser = sender === 'user';

  return (
    <div style={{
      display:"flex",
      justifyContent: isUser ? "flex-end" : "flex-start",
      width: "100%",
      alignItems:"flex-start",
      gap: "8px"
    }}>
      {!isUser && <Avatar icon={<RobotOutlined />} style={{ backgroundColor: "#1677ff"}}/>}
      <Card
        size='small'
        style={{
          maxWidth:"70%",
          background: isUser ? "#1677ff" :"#f0f0f0",
          color: isUser ? "#fff" : "#000",
          borderRadius:"10px"
        }}
      >
        <Text style={{color: isUser ? "#fff" : "#000"}}>{text}</Text>
      </Card>
        {isUser && <Avatar icon={<UserOutlined />} style={{ backgroundColor: "#87d068" }} />}
    </div>
  )
}

export default Message
