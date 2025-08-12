import './App.css';
import { Route, Routes } from "react-router-dom";
import PostDetail from './page/PostDetail';
import PostList from './page/PostList'




function App() {
  return (
    <div className="App">
      <Routes>
        <Route path='/' element={<PostList/>} />
        <Route path='/PostDetail/:id' element={<PostDetail/>} />
      </Routes>

    </div>
  );
}

export default App;