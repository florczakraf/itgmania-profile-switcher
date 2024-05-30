local ws = nil

local function Log(message, loggingMethod)
    loggingMethod = loggingMethod or Trace

    loggingMethod("ProfileSwitcher: " .. message)
end

local function SetLocalProfile(playerNumber, profileIndex)
    local topscreen = SCREENMAN:GetTopScreen()
    if type(topscreen["SetLocalProfile"]) == "function" then
		local resp = topscreen:SetLocalProfile(playerNumber, profileIndex)
		Log("SetLocalProfile returned: " .. resp)
	else
		Log("This screen doesn't support profile hot swapping.", Warn)
	end

end

local function ProfileSwitchActor(params)
    return Def.ActorFrame{
        Def.Quad{
            InitCommand=function(self)
                self:align(0, 0)
                self:diffuse(color("#00000000"))
            end,
            ResizeCommand=function(self)
                self:zoomto(0, 0)
            end,
        },
    }
end

ws = NETWORK:WebSocket{
    url="ws://localhost:5555/",
    pingInterval=30,
    automaticReconnect=true,
    onMessage=function(msg)
        local msgType = ToEnumShortString(msg.type)
        if msgType == "Open" then
			ws:Send("hello from itgmania")
            Log("Connected")
        elseif msgType == "Close" then
            Log("Dsiconnected")
        elseif msgType == "Error" then
            Log("Error")
        elseif msgType == "Message" then
			Log("Received message: " .. msg.data)
            local playerNumber, profileIndex = string.match(msg.data, "(%d+):(%d+)")
			if playerNumber == nil or profileIndex == nil then
                Log("playerNumber (" .. tostring(playerNumber) .. ") or profileIndex (" .. tostring(profileIndex) .. ") is undefined", Warn)
				return
			end

            Log("Swapping profile for player " .. playerNumber .. " to " .. profileIndex)
            SetLocalProfile(tonumber(playerNumber), tonumber(profileIndex))
        end

    end,
}

local t = {}
t["ScreenSelectMusic"] = ProfileSwitchActor{}
return t