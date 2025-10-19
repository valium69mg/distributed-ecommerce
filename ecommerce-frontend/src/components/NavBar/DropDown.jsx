import React from "react"

const dropDownStyle = {
    display: "flex",
    flexDirection: "column",
    position: "relative"
}

export default function DropDown({children, setState, isOpen, text = "More..."}) {
    return (
        <div style={dropDownStyle} onMouseEnter={() => setState(!isOpen)} onMouseLeave={() => setState(!isOpen)}>
            <span> {text} </span>
            {React.Children.map(children, child => React.isValidElement(child) ? React.cloneElement(child, { isOpen }) : child)}
        </div>
    )
}