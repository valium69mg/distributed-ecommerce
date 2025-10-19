const inputContainerStyle = {
    display: "flex",
    gap: "3px",
    marginLeft: "6px",
    alignItems: "center",
}

const inputStyle = {
    border: "none",
    outline: "none",
    width: "80%",
    color: "#686D76",
    marginBottom: "6px"
}

const iconStyle = {
  color: "#686D76",
  fontSize: "20px",
};

export default function InputField({icon, placeHolder="Type your email", onChange, value}) {
    return (
        <div style={inputContainerStyle}>
            <span style={iconStyle}>{icon ?? "x"}</span>
            <input style={inputStyle} type="text" placeholder={placeHolder} value={value} onChange={(event) => onChange(event.target.value)}/>
        </div>
    )
}