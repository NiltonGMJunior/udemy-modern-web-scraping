function main(splash, args)
    -- splash:set_user_agent("Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0")

    --[[
    headers = {
      ["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
    }
    splash:set_custom_headers(headers)
    ]] --

    splash:on_request(function(request)
        request:set_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0')
    end)

    url = args.url
    assert(splash:go(url))
    assert(splash:wait(1))

    input_box = assert(splash:select("#search_form_input_homepage"))
    input_box:focus()
    input_box:send_text("my user agent")
    assert(splash:wait(0.5))

    --[[
    search_button = assert(splash:select("#search_button_homepage"))
    search_button:mouse_click()
    ]] --

    input_box:send_keys("<Enter>")
    assert(splash:wait(1))

    splash:set_viewport_full()
    return {
        image = splash:png(),
        html = splash:html()
    }
end
