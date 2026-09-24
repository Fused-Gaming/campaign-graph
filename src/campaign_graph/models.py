from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import Any
from pydantic import BaseModel, Field


class NodeType(StrEnum):
    PERSON = "PERSON"
    NONPROFIT = "NONPROFIT"
    FOUNDATION = "FOUNDATION"
    PAC = "PAC"
    CAMPAIGN = "CAMPAIGN"
    GOVERNMENT_AGENCY = "GOVERNMENT_AGENCY"
    GOVERNMENT_OFFICIAL = "GOVERNMENT_OFFICIAL"
    LOBBYIST = "LOBBYIST"
    TRADE_ASSOCIATION = "TRADE_ASSOCIATION"
    DEVELOPER = "DEVELOPER"
    PROJECT = "PROJECT"
    CONTRACT = "CONTRACT"
    GRANT = "GRANT"
    PROPERTY = "PROPERTY"
    ADDRESS = "ADDRESS"
    DOCUMENT = "DOCUMENT"
    MEETING = "MEETING"
    VOTE = "VOTE"
    EVENT = "EVENT"


class VerificationStatus(StrEnum):
    DOCUMENTED = "DOCUMENTED"
    INFERRED = "INFERRED"
    UNRESOLVED = "UNRESOLVED"
    CONTRADICTED = "CONTRADICTED"


class Confidence(StrEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class EdgeType(StrEnum):
    BOARD_MEMBER = "BOARD_MEMBER"
    EMPLOYEE = "EMPLOYEE"
    OFFICER = "OFFICER"
    DONOR = "DONOR"
    CONTRIBUTION = "CONTRIBUTION"
    PAC_CONTRIBUTION = "PAC_CONTRIBUTION"
    INDEPENDENT_EXPENDITURE = "INDEPENDENT_EXPENDITURE"
    ENDORSED = "ENDORSED"
    LOBBIED = "LOBBIED"
    MET_WITH = "MET_WITH"
    FPC_ASSIGNED_TO = "FPC_ASSIGNED_TO"
    FUNDED = "FUNDED"
    GRANTED = "GRANTED"
    CONTRACTED_WITH = "CONTRACTED_WITH"
    DEVELOPMENT_PARTNER = "DEVELOPMENT_PARTNER"
    VOTED_YES = "VOTED_YES"
    VOTED_NO = "VOTED_NO"
    RECUSED = "RECUSED"
    ABSTAINED = "ABSTAINED"
    ABSENT = "ABSENT"
    PRESENT_NO_RECORDED_VOTE = "PRESENT_NO_RECORDED_VOTE"
    SHARED_ADDRESS = "SHARED_ADDRESS"
    SAME_BUILDING = "SAME_BUILDING"
    AUTHORED = "AUTHORED"
    RECEIVED = "RECEIVED"
    RECOMMENDED = "RECOMMENDED"
    APPROVED = "APPROVED"
    DISCLOSED_CONFLICT = "DISCLOSED_CONFLICT"
    RELATED_TO = "RELATED_TO"
    CAMPAIGN_VENDOR = "CAMPAIGN_VENDOR"
    COMMON_VENDOR = "COMMON_VENDOR"


MONEY_EDGE_TYPES = {EdgeType.CONTRIBUTION, EdgeType.PAC_CONTRIBUTION, EdgeType.INDEPENDENT_EXPENDITURE, EdgeType.FUNDED, EdgeType.GRANTED}
DECISION_EDGE_TYPES = {EdgeType.VOTED_YES, EdgeType.VOTED_NO, EdgeType.RECUSED, EdgeType.ABSTAINED, EdgeType.ABSENT, EdgeType.PRESENT_NO_RECORDED_VOTE, EdgeType.APPROVED, EdgeType.CONTRACTED_WITH}


class Evidence(BaseModel):
    source_url: str
    source_title: str
    source_date: date | None = None
    accessed_date: date
    source_type: str
    evidence_quote_or_summary: str
    confidence: Confidence
    verification_status: VerificationStatus


class Node(BaseModel):
    id: str
    label: str
    type: NodeType
    aliases: list[str] = Field(default_factory=list)
    identifiers: dict[str, str] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Edge(BaseModel):
    id: str
    source: str
    target: str
    type: EdgeType
    evidence: list[Evidence]
    amount: float | None = None
    currency: str | None = None
    date: date | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Event(BaseModel):
    id: str
    title: str
    date: date
    event_type: str
    node_ids: list[str] = Field(default_factory=list)
    edge_ids: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
