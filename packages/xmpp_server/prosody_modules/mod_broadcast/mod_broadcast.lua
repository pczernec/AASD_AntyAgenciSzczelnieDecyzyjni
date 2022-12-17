local from_address = module:get_option_string("broadcast_from");

function send_to_online(message)
	local c = 0;
	for hostname, host_session in pairs(hosts) do
		if host_session.sessions then
			for username in pairs(host_session.sessions) do
				c = c + 1;
				message.attr.to = username.."@"..hostname;
				module:send(message);
			end
		end
	end
	return c;
end

function send_message(event)
	local stanza = event.stanza;
	local from = stanza.attr.from;
    if from_address and from ~= from_address then
        -- stanza = st.clone(stanza);
        stanza.attr.from = from_address;
		local c = send_to_online(stanza);
		module:log("debug", "Broadcast stanza from %s to %d online users", from, c);
		return true;
    end
end

module:hook("message/bare", send_message);
