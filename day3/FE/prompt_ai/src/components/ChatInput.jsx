import React, { useState } from 'react'
import { Button, Input, Space } from 'antd';


const {TextArea} = Input 

const ChatInput = ({onSend}) => {

    const [input, setInput] = useState('')

    const handleSend = () => {
        if (input.trim()){
          onSend(input);
          setInput("");
        }
    };

  return (
    <Space.Compact style={{width:"100%"}}>
      <TextArea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder='Nhập tin nhắn ...'
        autoSize={{minRows:1, maxRows: 6}}// tự tăng chiều cao
        onPressEnter={(e) => {
          if(!e.shiftKey) {
            e.preventDefault() // ngăn chặn hành vi Enter
            handleSend()
          }
        }}
      />
      <Button type='primary' onClick={handleSend}>
        Submit
      </Button>
    </Space.Compact>
  )
}

export default ChatInput
