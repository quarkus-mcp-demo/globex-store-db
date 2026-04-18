--
-- PostgreSQL database dump
--

-- Dumped from database version 12.12
-- Dumped by pg_dump version 12.12

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: catalog; Type: TABLE; Schema: public; Owner: $POSTGRESQL_USER
--

CREATE TABLE public.catalog (
    item_id character varying(256) NOT NULL,
    name character varying(256),
    description text,
    category bigint,
    price double precision
);


ALTER TABLE public.catalog OWNER TO $POSTGRESQL_USER;

--
-- Name: catalog_tag; Type: TABLE; Schema: public; Owner: $POSTGRESQL_USER
--

CREATE TABLE public.catalog_tag (
    item_id character varying(256) NOT NULL,
    tag_id bigint NOT NULL
);


ALTER TABLE public.catalog_tag OWNER TO $POSTGRESQL_USER;

--
-- Name: category; Type: TABLE; Schema: public; Owner: $POSTGRESQL_USER
--

CREATE TABLE public.category (
    category_id bigint NOT NULL,
    category character varying(255)
);


ALTER TABLE public.category OWNER TO $POSTGRESQL_USER;

--
-- Name: inventory; Type: TABLE; Schema: public; Owner: $POSTGRESQL_USER
--

CREATE TABLE public.inventory (
    id bigint NOT NULL,
    itemid character varying(255),
    link character varying(255),
    location character varying(255), 
    quantity integer NOT NULL
);


ALTER TABLE public.inventory OWNER TO $POSTGRESQL_USER;

--
-- Name: inventory_sequence; Type: SEQUENCE; Schema: public; Owner: $POSTGRESQL_USER
--

CREATE SEQUENCE public.inventory_sequence
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.inventory_sequence OWNER TO $POSTGRESQL_USER;

--
-- Name: tag; Type: TABLE; Schema: public; Owner: $POSTGRESQL_USER
--

CREATE TABLE public.tag (
    tag_id bigint NOT NULL,
    tag character varying(255)
);


ALTER TABLE public.tag OWNER TO $POSTGRESQL_USER;

--
-- Name: inventory inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: $POSTGRESQL_USER
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_pkey PRIMARY KEY (id);


--
-- Name: catalog pk_catalog; Type: CONSTRAINT; Schema: public; Owner: $POSTGRESQL_USER
--

ALTER TABLE ONLY public.catalog
    ADD CONSTRAINT pk_catalog PRIMARY KEY (item_id);


--
-- Name: catalog_tag pk_catalog_tag; Type: CONSTRAINT; Schema: public; Owner: $POSTGRESQL_USER
--

ALTER TABLE ONLY public.catalog_tag
    ADD CONSTRAINT pk_catalog_tag PRIMARY KEY (item_id, tag_id);


--
-- Name: category pk_category; Type: CONSTRAINT; Schema: public; Owner: $POSTGRESQL_USER
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT pk_category PRIMARY KEY (category_id);


--
-- Name: tag pk_tag; Type: CONSTRAINT; Schema: public; Owner: $POSTGRESQL_USER
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT pk_tag PRIMARY KEY (tag_id);


--
-- Name: catalog fk_category; Type: FK CONSTRAINT; Schema: public; Owner: $POSTGRESQL_USER
--

ALTER TABLE ONLY public.catalog
    ADD CONSTRAINT fk_category FOREIGN KEY (category) REFERENCES public.category(category_id);


--
-- Name: address; Type: TABLE; Schema: public; Owner: $POSTGRESQL_USER
--

CREATE TABLE public.address (
    cust_id bigint NOT NULL,
    address1 character varying(255),
    address2 character varying(255),
    city character varying(255),
    zip character varying(10),
    state character varying(10),
    country character varying(30)
);


ALTER TABLE public.address OWNER TO $POSTGRESQL_USER;

--
-- Name: customer; Type: TABLE; Schema: public; Owner: $POSTGRESQL_USER
--

CREATE TABLE public.customer (
    id bigint NOT NULL,
    user_id character varying(20),
    first_name character varying(255),
    last_name character varying(255),
    email character varying(255),
    phone character varying(20)
);


ALTER TABLE public.customer OWNER TO $POSTGRESQL_USER;

--
-- Name: payment; Type: TABLE; Schema: public; Owner: $POSTGRESQL_USER
--

CREATE SEQUENCE public.customer_id_seq
    START WITH 1000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.customer_id_seq OWNER TO $POSTGRESQL_USER;

--
-- Name: address address_pkey; Type: CONSTRAINT; Schema: public; Owner: $POSTGRESQL_USER
--

ALTER TABLE ONLY public.address
    ADD CONSTRAINT address_pkey PRIMARY KEY (cust_id);


--
-- Name: customer customer_pkey; Type: CONSTRAINT; Schema: public; Owner: $POSTGRESQL_USER
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (id);


--
-- Name: address fkfl3q6evy823xno4batlhd8jne; Type: FK CONSTRAINT; Schema: public; Owner: $POSTGRESQL_USER
--

ALTER TABLE ONLY public.address
    ADD CONSTRAINT fkfl3q6evy823xno4batlhd8jne FOREIGN KEY (cust_id) REFERENCES public.customer(id);


--
-- Name: customer customer_email; Type: CONSTRAINT; Schema: public; Owner: $POSTGRESQL_USER
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_email UNIQUE (email);


--
-- Name: customer customer_email; Type: CONSTRAINT; Schema: public; Owner: $POSTGRESQL_USER
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_user_id UNIQUE (user_id);


--
-- Name: line_item; Type: TABLE; Schema: public; Owner: $POSTGRESQL_USER
--

CREATE TABLE public.line_item (
    id bigint NOT NULL,
    price numeric(8,2),
    product_code character varying(30),
    quantity integer,
    order_id bigint
);


ALTER TABLE public.line_item OWNER TO $POSTGRESQL_USER;

--
-- Name: line_item_id_seq; Type: SEQUENCE; Schema: public; Owner: $POSTGRESQL_USER
--

CREATE SEQUENCE public.line_item_id_seq
    START WITH 6000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.line_item_id_seq OWNER TO $POSTGRESQL_USER;


--
-- Name: order_id_seq; Type: SEQUENCE; Schema: public; Owner: $POSTGRESQL_USER
--

CREATE SEQUENCE public.order_id_seq
    START WITH 3000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.order_id_seq OWNER TO $POSTGRESQL_USER;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: $POSTGRESQL_USER
--

CREATE TABLE public.orders (
    id bigint NOT NULL,
    customer_id character varying(30),
    order_ts timestamp without time zone
);


ALTER TABLE public.orders OWNER TO $POSTGRESQL_USER;
--
-- Name: shipping_address; Type: TABLE; Schema: public; Owner: $POSTGRESQL_USER
--

CREATE TABLE public.shipping_address (
    id bigint NOT NULL,
    address1 character varying(100),
    address2 character varying(100),
    city character varying(50),
    country character varying(30),
    name character varying(100),
    phone character varying(30),
    state character varying(30),
    zip character varying(30),
    order_id bigint
);


ALTER TABLE public.shipping_address OWNER TO $POSTGRESQL_USER;

--
-- Name: shipping_address_id_seq; Type: SEQUENCE; Schema: public; Owner: $POSTGRESQL_USER
--

CREATE SEQUENCE public.shipping_address_id_seq
    START WITH 3000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.shipping_address_id_seq OWNER TO $POSTGRESQL_USER;

--
-- Name: line_item line_item_pkey; Type: CONSTRAINT; Schema: public; Owner: $POSTGRESQL_USER
--

ALTER TABLE ONLY public.line_item
    ADD CONSTRAINT line_item_pkey PRIMARY KEY (id);


--
-- Name: order order_pkey; Type: CONSTRAINT; Schema: public; Owner: $POSTGRESQL_USER
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT order_pkey PRIMARY KEY (id);


--
-- Name: shipping_address shipping_address_pkey; Type: CONSTRAINT; Schema: public; Owner: $POSTGRESQL_USER
--

ALTER TABLE ONLY public.shipping_address
    ADD CONSTRAINT shipping_address_pkey PRIMARY KEY (id);


--
-- Name: shipping_address fkl88fq4d2ypn9qvg8x90uimnca; Type: FK CONSTRAINT; Schema: public; Owner: $POSTGRESQL_USER
--

ALTER TABLE ONLY public.shipping_address
    ADD CONSTRAINT fkl88fq4d2ypn9qvg8x90uimnca FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- Name: line_item fklfuo9o3keu9a7mlxumaqoylgu; Type: FK CONSTRAINT; Schema: public; Owner: $POSTGRESQL_USER
--

ALTER TABLE ONLY public.line_item
    ADD CONSTRAINT fklfuo9o3keu9a7mlxumaqoylgu FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- PostgreSQL database dump complete
--

--
-- MCP Demo POC
--

--- enums

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'sessionstatus') THEN
        CREATE TYPE public.sessionstatus AS ENUM ('ACTIVE', 'INACTIVE', 'EXPIRED', 'ARCHIVED');
    END IF;
END
$$;

-- request_sessions
CREATE TABLE IF NOT EXISTS public.request_sessions (
    id BIGINT NOT NULL,
    session_id VARCHAR(36) NOT NULL,
    user_id TEXT NOT NULL,
    status public.sessionstatus NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    current_agent_id TEXT,
    conversation_thread_id TEXT,
    conversation_checkpoint_id TEXT,
    version INTEGER
);
ALTER TABLE ONLY public.request_sessions ADD CONSTRAINT pkey_request_sessions PRIMARY KEY (id);
ALTER TABLE ONLY public.request_sessions ADD CONSTRAINT unique_session_id UNIQUE (session_id);
ALTER TABLE ONLY public.request_sessions ADD CONSTRAINT unique_user_id UNIQUE (user_id);
CREATE INDEX IF NOT EXISTS ix_session_id ON public.request_sessions (session_id);
CREATE INDEX IF NOT EXISTS ix_request_sessions_user_id ON public.request_sessions (user_id);

ALTER TABLE public.request_sessions OWNER TO $POSTGRESQL_USER;

CREATE SEQUENCE public.request_sessions_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.request_sessions_seq OWNER TO $POSTGRESQL_USER;

-- Langraph4J Postgres Saver
CREATE TABLE IF NOT EXISTS public.LG4JThread (
    thread_id UUID PRIMARY KEY,
    thread_name VARCHAR(255),
    is_released BOOLEAN DEFAULT FALSE NOT NULL
);

ALTER TABLE public.LG4JThread OWNER TO $POSTGRESQL_USER;

CREATE TABLE IF NOT EXISTS public.LG4JCheckpoint (
    checkpoint_id UUID PRIMARY KEY,
    parent_checkpoint_id UUID,
    thread_id UUID NOT NULL,
    node_id VARCHAR(255),
    next_node_id VARCHAR(255),
    state_data JSONB NOT NULL,
    state_content_type VARCHAR(100) NOT NULL, 
    saved_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_thread
        FOREIGN KEY(thread_id)
        REFERENCES public.LG4JThread(thread_id)
        ON DELETE CASCADE
);

ALTER TABLE public.LG4JCheckpoint OWNER TO $POSTGRESQL_USER;

CREATE INDEX IF NOT EXISTS idx_lg4jcheckpoint_thread_id ON public.LG4JCheckpoint(thread_id);
CREATE INDEX IF NOT EXISTS idx_lg4jcheckpoint_thread_id_saved_at_desc ON public.LG4JCheckpoint(thread_id, saved_at DESC);
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_lg4jthread_thread_name_unreleased  ON public.LG4JThread(thread_name) WHERE is_released = FALSE;

-- complaints
CREATE TABLE IF NOT EXISTS public.complaints (
    id BIGINT NOT NULL,
    user_id TEXT,
    order_id BIGINT,
    product_code TEXT,
    issue_type TEXT,
    severity TEXT,
    complaint TEXT,
    status TEXT,
    resolution TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    version INTEGER
);

ALTER TABLE ONLY public.complaints ADD CONSTRAINT pkey_complaints PRIMARY KEY (id);
CREATE INDEX IF NOT EXISTS ix_complaints_order_id ON public.complaints (order_id);
CREATE INDEX IF NOT EXISTS ix_complaints_status ON public.complaints (status);

ALTER TABLE public.complaints OWNER TO $POSTGRESQL_USER;

CREATE SEQUENCE public.complaints_seq
    START WITH 2500
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.complaints_seq OWNER TO $POSTGRESQL_USER;
