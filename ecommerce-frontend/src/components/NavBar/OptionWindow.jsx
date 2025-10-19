
const windowHidden = {
    visibility: "hidden"
}

const windowStyle = {
    display: "grid",
    gridTemplateColumns: "1fr",
    gap: "3px",
    position: "absolute",
    top: "100%",
    left: "0",
    border: "1px solid black",
    padding: "6px 12px"

}

function getOptionWindowStyle(isOpen) {
    if (isOpen) {
        return windowStyle;
    }
    return {...windowStyle, ...windowHidden}
}

export default function OptionWindow({isOpen = true, children}) {
    return (
        <div style={getOptionWindowStyle(isOpen)}> 
            {children}
        </div>
    )
}