import React, { useRef } from "react";

const dropDownStyle = {
  display: "flex",
  flexDirection: "column",
  position: "relative",
  fontSize: "18px",
};

export default function DropDown({ children, setState, isOpen, text = "More..." }) {
  const timeoutRef = useRef(null);

  return (
    <div
      style={dropDownStyle}
      onMouseEnter={() => {
        clearTimeout(timeoutRef.current);
        setState(true);
      }}
      onMouseLeave={() => {
        timeoutRef.current = setTimeout(() => setState(false), 100);
      }}
    >
      <span>{text}</span>
      {React.Children.map(children, child =>
        React.isValidElement(child) ? React.cloneElement(child, { isOpen }) : child
      )}
    </div>
  );
}
