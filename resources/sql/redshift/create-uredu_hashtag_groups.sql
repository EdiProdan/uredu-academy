CREATE TABLE IF NOT EXISTS "uredu-academy-final-schema".hashtag_groups (
    id INTEGER IDENTITY(1,1) PRIMARY KEY,
    group_name VARCHAR(255),
    hashtag_name VARCHAR(255)
);

-- Insert data for all groups and hashtags
INSERT INTO "uredu-academy-final-schema".hashtag_groups (group_name, hashtag_name)
VALUES
--Football
('Football', 'fifaworldcup'),
('Football', 'qatar2022'),
('Football', 'vatreni'),
('Football', 'family'),
('Football', 'hrv'),
('Football', 'worldcup'),
('Football', 'nationsleague'),
('Football', 'unl'),
('Football', 'hnl'),
('Football', 'supersporthnl'),
('Football', 'euro2024'),
('Football', 'uclfinal'),
('Football', 'uyl'),
('Football', 'youthleague'),
('Football', 'dinamozagreb'),

--Sport
('Sport', 'kkcibona'),
('Sport', 'crobeachhandball'),
('Sport', 'bheuro2023'),
('Sport', 'rukometnapijesku'),
('Sport', 'rolandgarros'),
('Sport', 'wta'),
('Sport', 'frenchopen'),
('Sport', 'ufc280'),
('Sport', 'superbowl'),
('Sport', 'sehaleague'),
('Sport', 'ufc287'),
('Sport', 'parisroubaix'),

--Eurovision
('Eurovision', 'eurovision2023'),
('Eurovision', 'eurovision'),
('Eurovision', 'dora2023'),
('Eurovision', 'sanremo2023'),

-- Streaming
('Streaming', 'percyhyneswhite'),
('Streaming', 'wavier'),
('Streaming', 'wednesdaynetflix'),
('Streaming', 'netflix'),
('Streaming', 'warriornun'),
('Streaming', 'warriornunsaved'),
('Streaming', '911onfox'),
('Streaming', 'houseofthedragon'),
('Streaming', 'mariachis'),
('Streaming', 'thelastofus'),
('Streaming', 'socspinoff'),
('Streaming', 'tvtime'),
('Streaming', 'doctorwho'),

-- Crypto/NFTs
('Crypto/NFTs', 'nft'),
('Crypto/NFTs', 'nfts'),
('Crypto/NFTs', 'nftcommunity'),
('Crypto/NFTs', 'eth'),
('Crypto/NFTs', 'nftgiveaway'),
('Crypto/NFTs', 'ethereum'),
('Crypto/NFTs', 'bayc'),
('Crypto/NFTs', 'bitcoin'),
('Crypto/NFTs', 'sec'),
('Crypto/NFTs', 'crypto'),

-- Writers/readers
('Writers/readers', 'writerslift'),
('Writers/readers', 'kindle'),
('Writers/readers', 'books'),
('Writers/readers', 'kindlebooks'),
('Writers/readers', 'knjiga'),
('Writers/readers', 'reading'),
('Writers/readers', 'freebook'),
('Writers/readers', 'amreading'),
('Writers/readers', 'wattpad'),

-- Finance
('Finance', 'finance'),
('Finance', 'economics'),
('Finance', 'market'),
('Finance', 'money'),

-- Asian celebrities
('Asian celebrities', 'acoty2022'),
('Asian celebrities', 'netizensreport'),
('Asian celebrities', 'jungkook'),
('Asian celebrities', 'bts'),
('Asian celebrities', 'jin'),
('Asian celebrities', 'jimin'),
('Asian celebrities', 'btswrappedparty'),

-- Photography
('Photography', 'photography'),
('Photography', 'photooftheday'),
('Photography', 'streetphotography'),
('Photography', 'naturephotography'),
('Photography', 'landscapephotography'),
('Photography', 'travelphotography'),

-- Traveling
('Traveling', 'travel'),
('Traveling', 'travelcroatia'),
('Traveling', 'travelphotography'),
('Traveling', 'bestintravel'),
('Traveling', 'travelblog'),

-- Technology
('Technology', 'technology'),
('Technology', 'business'),
('Technology', 'racunalo'),
('Technology', 'marketing'),
('Technology', 'smartphone'),
('Technology', 'rebootdevelop'),
('Technology', 'ai'),

-- Science
('Science', 'uranium'),
('Science', 'nuclearenergy'),
('Science', 'exploration'),
('Science', 'silver'),
('Science', 'copper'),
('Science', 'artemis'),

-- RealityTV
('RealityTV', 'survivorhrvatska'),
('RealityTV', 'survivorsrbija'),
('RealityTV', 'loveisland'),
('RealityTV', 'zadruga6'),

-- Racing
('Racing', 'f1'),
('Racing', 'ff16'),
('Racing', 'f1driveroftheday'),
('Racing', 'formula1'),
('Racing', 'japanesegp'),
('Racing', 'wrc'),

-- Music
('Music', 'iheartawards'),
('Music', 'bestmusicvideo'),
('Music', 'spotifywrapped'),
('Music', 'spotify'),
('Music', 'amas'),
('Music', 'amasfanfavorite'),
('Music', 'grammys'),
('Music', 'hot100'),
('Music', 'soundcloud'),

-- Creative
('Creative', 'pixelart'),
('Creative', 'digitalart'),
('Creative', 'artistsontwitter'),
('Creative', 'furryart'),
('Creative', 'art'),
('Creative', 'portfolioday'),
('Creative', 'etsy'),
('Creative', 'etsyshop'),
('Creative', 'handmade'),
('Creative', 'framemockups'),
('Creative', 'design'),
('Creative', 'artprints'),
('Creative', 'comics'),

-- Movie
('Movie', 'movie'),
('Movie', 'script'),
('Movie', 'movieaudition'),
('Movie', 'filmmaker'),
('Movie', 'screenplay'),
('Movie', 'film'),
('Movie', 'cinema'),
('Movie', 'oscars'),

-- Politics
('Politics', 'standwithukraine'),
('Politics', 'ukrainerussianwar'),
('Politics', 'russiaukraineconflict'),
('Politics', 'schengen'),
('Politics', 'bloombergadria'),
('Politics', 'helpsyria'),
('Politics', 'cop27'),
('Politics', 'dubrovnikforum2023'),
('Politics', 'coronation'),
('Politics', 'eucivilprotection'),
('Politics', 'croatiathepearl'),
('Politics', 'wef23'),
('Politics', 'eurozone'),

-- Gaming
('Gaming', 'roblox'),
('Gaming', 'robloxdev'),
('Gaming', 'gaming_news'),
('Gaming', 'gaming'),
('Gaming', 'pcgaming'),
('Gaming', 'steam'),
('Gaming', 'indiegame'),
('Gaming', 'twitch'),
('Gaming', 'rebootdevelop'),
('Gaming', 'dreamfacereveal'),
('Gaming', 'diabloiv'),
('Gaming', 'ps5share');