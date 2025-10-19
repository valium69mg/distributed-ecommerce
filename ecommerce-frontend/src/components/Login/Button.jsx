const buttonStyle = {
    width: "70%",
    height: "28px",
    border: "1px solid black",
    marginTop: "24px",
    textAlign: "center",
    cursor: "pointer",
    borderRadius: "3px",
    display: "flex",           
    alignItems: "center",       
    justifyContent: "center"    
}

export default function Button({buttonText = "Input", onClick}) {
    return (
        <div style={buttonStyle} onClick={() => onClick()}>
            {buttonText}
        </div>
    )
}