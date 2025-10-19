const searchBarStyle = {
    width: "40%"
}

const inputStyle = {
    border: "none",
    outline: "none",
    width: "80%",
    color: "#686D76"
}

export default function SearchBar() {
    return (
        <div style={searchBarStyle}>
            <span> x </span>
            <input style={inputStyle} type="text" value="" placeholder="What are you searching for?"/>
        </div>
    )
}