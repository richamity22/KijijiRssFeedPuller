CREATE TABLE "results" (
	"search_id"	TEXT NOT NULL,
	"http_addr"	TEXT NOT NULL,
	"out_text"	TEXT NOT NULL,
	"is_ok"	INTEGER NOT NULL,
	PRIMARY KEY("search_id")
);

CREATE TABLE "searches" (
	"recID"	INTEGER NOT NULL,
	"http_addr"	TEXT NOT NULL,
	"mail_title"	TEXT,
	"mail_to"	TEXT NOT NULL,
	"cc_to"	TEXT,
	"last_search"	TEXT,
	"active"	TEXT NOT NULL DEFAULT 'Y',
	PRIMARY KEY("recID")
);

INSERT INTO 
searches(recID, http_addr, mail_title, mail_to, cc_to, last_search, active) 
VALUES(1,"https://www.kijiji.ca/rss-srp-hot-tub-pool/ontario/heater/k0c681l9004",
"Heaters on Kijiji","richamity22@gmail.com","","","Y");

