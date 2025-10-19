const userSettingsStyle = {
    width: "20%"
}

export default function UserSettings({children}) {
    return (
        <div style={userSettingsStyle}>
            {children}
        </div> 
    )
}