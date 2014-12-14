(import requests json os)
(import [ConfigParser [SafeConfigParser]])

(setv parser (SafeConfigParser()))
(parser.read (os.path.join (os.path.expanduser "~") ".umbrellarc"))

(setv api_key (parser.get "weather" "api_key"))
(setv state (parser.get "weather" "state"))
(setv city (parser.get "weather" "city"))
(setv hour_cap (parser.get "weather" "hour_cap"))
(setv endpoint (+ "http://api.wunderground.com/api/" api_key "/hourly/q/" state "/" city ".json"))

(setv weather (requests.get endpoint))
(setv parsed_json (json.loads weather.text))

(if (= weather.status_code 200)
    (do 
        (for [ [hour_index hours] (enumerate (get parsed_json "hourly_forecast")) ]
            (if (> hour_index (int hour_cap))
                (do
                    (print (+
                                (.strip (-> (get hours "FCTTIME") (get "civil"))) " :: "
                                (.strip (-> (get hours "temp") (get "english"))) "F :: "
                                (.strip (-> (get hours "pop"))) "%"
                            )
                    )
                )
            )
        )
    )
)
