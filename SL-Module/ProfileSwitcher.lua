local SERVER_URL = "ws://localhost:5555/"

local function Log(message, loggingMethod)
    -- Use this function for prefixed logging within the module.
    -- Known logging methods: Trace (default), Warn, SM

    loggingMethod = loggingMethod or Trace

    loggingMethod("ProfileSwitcher: " .. message)
end

local function SetLocalProfile(playerNumber, profileIndex)
    local topscreen = SCREENMAN:GetTopScreen()

    if topscreen == nil then  -- happens on startup
        Log("topscreen not available yet")
        return

    end
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
            ModuleCommand=function(self)
                -- Uncomment and modify the following commands to load some
                -- default profiles on every song wheel load:

                -- SetLocalProfile(0, 0)
                -- SetLocalProfile(1, 1)
            end
        },
    }
end

local ws = nil
ws = NETWORK:WebSocket{
    url=SERVER_URL,
    pingInterval=30,
    automaticReconnect=true,
    onMessage=function(msg)
        local msgType = ToEnumShortString(msg.type)
        if msgType == "Open" then
            ws:Send("hello from itgmania")
            Log("Connected")
        elseif msgType == "Close" then
            Log("Disconnected")
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