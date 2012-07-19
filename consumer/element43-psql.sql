--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: emdrJsonmessages; Type: TABLE; Schema: public; Owner: element43; Tablespace: 
--

CREATE TABLE "emdrJsonmessages" (
    "msgKey" character(36) NOT NULL,
    "msgReceived" timestamp without time zone NOT NULL,
    "msgType" character varying(16) DEFAULT NULL::character varying,
    message bytea
);


ALTER TABLE public."emdrJsonmessages" OWNER TO element43;

--
-- Name: emdrStats; Type: TABLE; Schema: public; Owner: element43; Tablespace: 
--

CREATE TABLE "emdrStats" (
    id bigint NOT NULL,
    "statusType" smallint DEFAULT 0::smallint NOT NULL,
    "statusCount" integer DEFAULT 0 NOT NULL,
    "messageTimestamp" timestamp without time zone NOT NULL
);


ALTER TABLE public."emdrStats" OWNER TO element43;

--
-- Name: emdrStatsWorking; Type: TABLE; Schema: public; Owner: element43; Tablespace: 
--

CREATE TABLE "emdrStatsWorking" (
    id bigint NOT NULL,
    "statusType" smallint DEFAULT 0::smallint NOT NULL
);


ALTER TABLE public."emdrStatsWorking" OWNER TO element43;

--
-- Name: historicalData; Type: TABLE; Schema: public; Owner: element43; Tablespace: 
--

CREATE TABLE "historicalData" (
    "uniqueKey" character varying(36) NOT NULL,
    "regionID" integer NOT NULL,
    "typeID" integer NOT NULL,
    "historyData" bytea NOT NULL
);


ALTER TABLE public."historicalData" OWNER TO element43;

--
-- Name: marketData; Type: TABLE; Schema: public; Owner: element43; Tablespace: 
--

CREATE TABLE "marketData" (
    "generatedAt" timestamp without time zone,
    "regionID" integer NOT NULL,
    "typeID" integer NOT NULL,
    price double precision NOT NULL,
    "volumeRemaining" integer NOT NULL,
    "volumeEntered" integer NOT NULL,
    "minimumVolume" bigint NOT NULL,
    range smallint NOT NULL,
    "orderID" bigint NOT NULL,
    bid smallint NOT NULL,
    "issueDate" timestamp without time zone NOT NULL,
    duration smallint NOT NULL,
    "stationID" bigint NOT NULL,
    "solarSystemID" bigint NOT NULL,
    suspicious character(1) DEFAULT '?'::bpchar NOT NULL,
    "msgKey" character varying(36) DEFAULT NULL::character varying,
    "ipHash" character varying(48) DEFAULT NULL::character varying
);


ALTER TABLE public."marketData" OWNER TO element43;

--
-- Name: marketDataWarehouse; Type: TABLE; Schema: public; Owner: element43; Tablespace: 
--

CREATE TABLE "marketDataWarehouse" (
    "generatedAt" timestamp without time zone,
    "regionID" integer NOT NULL,
    "typeID" integer NOT NULL,
    price double precision NOT NULL,
    "volumeEntered" integer NOT NULL,
    range smallint NOT NULL,
    "orderID" integer NOT NULL,
    bid smallint NOT NULL,
    "issueDate" timestamp without time zone NOT NULL,
    duration smallint NOT NULL,
    "stationID" integer NOT NULL,
    "solarSystemID" integer NOT NULL,
    suspicious character(1) DEFAULT '?'::bpchar NOT NULL,
    "completeTime" timestamp without time zone DEFAULT now() NOT NULL,
    "ipHash" character varying(48) DEFAULT NULL::character varying
);


ALTER TABLE public."marketDataWarehouse" OWNER TO element43;

--
-- Name: seenOrders; Type: TABLE; Schema: public; Owner: element43; Tablespace: 
--

CREATE TABLE "seenOrders" (
    "orderID" bigint NOT NULL,
    "typeID" integer NOT NULL,
    "regionID" integer NOT NULL,
    bid smallint NOT NULL
);


ALTER TABLE public."seenOrders" OWNER TO element43;

--
-- Name: seenOrdersWorking; Type: TABLE; Schema: public; Owner: element43; Tablespace: 
--

CREATE TABLE "seenOrdersWorking" (
    "orderID" bigint NOT NULL,
    "typeID" integer NOT NULL,
    "regionID" integer NOT NULL,
    bid smallint NOT NULL
);


ALTER TABLE public."seenOrdersWorking" OWNER TO element43;

--
-- Data for Name: emdrJsonmessages; Type: TABLE DATA; Schema: public; Owner: element43
--

COPY "emdrJsonmessages" ("msgKey", "msgReceived", "msgType", message) FROM stdin;
\.


--
-- Data for Name: emdrStats; Type: TABLE DATA; Schema: public; Owner: element43
--

COPY "emdrStats" (id, "statusType", "statusCount", "messageTimestamp") FROM stdin;
\.


--
-- Data for Name: emdrStatsWorking; Type: TABLE DATA; Schema: public; Owner: element43
--

COPY "emdrStatsWorking" (id, "statusType") FROM stdin;
\.


--
-- Data for Name: historicalData; Type: TABLE DATA; Schema: public; Owner: element43
--

COPY "historicalData" ("uniqueKey", "regionID", "typeID", "historyData") FROM stdin;
\.


--
-- Data for Name: marketData; Type: TABLE DATA; Schema: public; Owner: element43
--

COPY "marketData" ("generatedAt", "regionID", "typeID", price, "volumeRemaining", "volumeEntered", "minimumVolume", range, "orderID", bid, "issueDate", duration, "stationID", "solarSystemID", suspicious, "msgKey", "ipHash") FROM stdin;
\.


--
-- Data for Name: marketDataWarehouse; Type: TABLE DATA; Schema: public; Owner: element43
--

COPY "marketDataWarehouse" ("generatedAt", "regionID", "typeID", price, "volumeEntered", range, "orderID", bid, "issueDate", duration, "stationID", "solarSystemID", suspicious, "completeTime", "ipHash") FROM stdin;
\.


--
-- Data for Name: seenOrders; Type: TABLE DATA; Schema: public; Owner: element43
--

COPY "seenOrders" ("orderID", "typeID", "regionID", bid) FROM stdin;
\.


--
-- Data for Name: seenOrdersWorking; Type: TABLE DATA; Schema: public; Owner: element43
--

COPY "seenOrdersWorking" ("orderID", "typeID", "regionID", bid) FROM stdin;
\.


--
-- Name: emdrJsonmessages_pkey; Type: CONSTRAINT; Schema: public; Owner: element43; Tablespace: 
--

ALTER TABLE ONLY "emdrJsonmessages"
    ADD CONSTRAINT "emdrJsonmessages_pkey" PRIMARY KEY ("msgKey");


--
-- Name: emdrStatsWorking_pkey; Type: CONSTRAINT; Schema: public; Owner: element43; Tablespace: 
--

ALTER TABLE ONLY "emdrStatsWorking"
    ADD CONSTRAINT "emdrStatsWorking_pkey" PRIMARY KEY (id);


--
-- Name: emdrStats_pkey; Type: CONSTRAINT; Schema: public; Owner: element43; Tablespace: 
--

ALTER TABLE ONLY "emdrStats"
    ADD CONSTRAINT "emdrStats_pkey" PRIMARY KEY (id);


--
-- Name: historicalData_pkey; Type: CONSTRAINT; Schema: public; Owner: element43; Tablespace: 
--

ALTER TABLE ONLY "historicalData"
    ADD CONSTRAINT "historicalData_pkey" PRIMARY KEY ("uniqueKey");


--
-- Name: marketDataWarehouse_pkey; Type: CONSTRAINT; Schema: public; Owner: element43; Tablespace: 
--

ALTER TABLE ONLY "marketDataWarehouse"
    ADD CONSTRAINT "marketDataWarehouse_pkey" PRIMARY KEY ("orderID");


--
-- Name: marketData_pkey; Type: CONSTRAINT; Schema: public; Owner: element43; Tablespace: 
--

ALTER TABLE ONLY "marketData"
    ADD CONSTRAINT "marketData_pkey" PRIMARY KEY ("orderID");


--
-- Name: seenOrdersWorking_pkey; Type: CONSTRAINT; Schema: public; Owner: element43; Tablespace: 
--

ALTER TABLE ONLY "seenOrdersWorking"
    ADD CONSTRAINT "seenOrdersWorking_pkey" PRIMARY KEY ("orderID");


--
-- Name: seenOrders_pkey; Type: CONSTRAINT; Schema: public; Owner: element43; Tablespace: 
--

ALTER TABLE ONLY "seenOrders"
    ADD CONSTRAINT "seenOrders_pkey" PRIMARY KEY ("orderID");


--
-- Name: generatedAt; Type: INDEX; Schema: public; Owner: element43; Tablespace: 
--

CREATE INDEX "generatedAt" ON "marketData" USING btree ("generatedAt");


--
-- Name: regionID; Type: INDEX; Schema: public; Owner: element43; Tablespace: 
--

CREATE INDEX "regionID" ON "marketData" USING btree ("regionID");


--
-- Name: typeID; Type: INDEX; Schema: public; Owner: element43; Tablespace: 
--

CREATE INDEX "typeID" ON "marketData" USING btree ("typeID");


--
-- Name: typeID_regionID; Type: INDEX; Schema: public; Owner: element43; Tablespace: 
--

CREATE INDEX "typeID_regionID" ON "marketData" USING btree ("typeID", "regionID");


--
-- Name: typeID_solarSystemID; Type: INDEX; Schema: public; Owner: element43; Tablespace: 
--

CREATE INDEX "typeID_solarSystemID" ON "marketData" USING btree ("typeID", "solarSystemID");


--
-- Name: typeID_stationID; Type: INDEX; Schema: public; Owner: element43; Tablespace: 
--

CREATE INDEX "typeID_stationID" ON "marketData" USING btree ("typeID", "stationID");


--
-- Name: typeID_stationID_bid_price_volumeRemaining; Type: INDEX; Schema: public; Owner: element43; Tablespace: 
--

CREATE INDEX "typeID_stationID_bid_price_volumeRemaining" ON "marketData" USING btree ("typeID", "stationID", bid, price, "volumeRemaining");


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

