
const windowHidden = {
    visibility: "hidden"
}



function getOptionWindowStyle(isOpen, windowStyle, windowHidden) {
    if (isOpen) {
        return windowStyle;
    }
    return {...windowStyle, ...windowHidden}
}

export default function OptionWindow({isOpen = true, width = "180px", children}) {
    
    const windowStyle = {
        display: "grid",
        gridTemplateColumns: "1fr",
        gap: "6px",
        position: "absolute",
        top: "100%",
        left: "0",
        padding: "12px 24px",
        backgroundColor: 'whitesmoke',
        boxShadow: "0px 0px 6px 0px rgba(0,0,0,0.5)",
        width: width,
        marginTop: "12px"
    }

    return (
        <div style={getOptionWindowStyle(isOpen, windowStyle, windowHidden)}> 
            {children}
        </div>
    )
}