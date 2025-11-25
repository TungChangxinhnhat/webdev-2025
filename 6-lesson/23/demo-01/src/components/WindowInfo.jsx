import { useState, useEffect } from "react";

export default function WindowInfo() {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    document.title = `Ширина: ${width}px`;
  }, [width]);

  useEffect(() => {
    function handleResize() {
      setWidth(window.innerWidth);
    }

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return <p>Текущая ширина окна: {width}px</p>;
}
