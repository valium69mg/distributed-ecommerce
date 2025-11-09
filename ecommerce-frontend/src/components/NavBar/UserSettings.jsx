import { RiAccountCircleLine } from "react-icons/ri";

const userSettingsStyle = {
    width: "30%",
}

const userSettinsDropDownStyle = {
    display: "flex",
    alignItems: "center",
    gap: "6px",
    paddingLeft: "45%"
}

export default function UserSettings({children}) {
    return (
        <div style={userSettingsStyle}>
            <div style={userSettinsDropDownStyle}>
                <RiAccountCircleLine size={36} />
                {children}
            </div>
        </div> 
    )
}