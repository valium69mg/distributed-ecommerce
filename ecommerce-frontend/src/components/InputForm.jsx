
const containerStyle = {
    display: "flex",
    flexDirection: "column",
    //border: "solid 1px red",
    width: "80%",
}

const underLineStype = {
    width: "100%",
    borderBottom: "solid 2px #CBCBCB",
    height: "100%",
    marginTop: "12px"

}

export default function InputForm({inputField = "Email", children}) {
    return (
        <div style={containerStyle}>
            <p> {inputField} </p>
            {children}
            <span style={underLineStype}></span>
        </div>
    )
}

