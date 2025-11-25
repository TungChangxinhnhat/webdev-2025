import Counter from "./components/Counter.jsx";
import Posts from "./components/Posts.jsx";
import UserPanel from "./components/UserPanel.jsx";
import WindowInfo from "./components/WindowInfo.jsx";

export default function App() {
  return (
    <>
        <WindowInfo/>
        <Counter/>
        <UserPanel isLoading={true}/>
        <Posts/>
    </>
  );
}
