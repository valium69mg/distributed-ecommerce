const anchorLinkStyle = {
    fontSize: "18px"
}

export default function AnchorLink({linkName = "Link"}) {
    return (
        <a style={anchorLinkStyle}> {linkName} </a>
    )
}