import re
import locale
import warnings
import numpy as np
import pandas as pd
from ncls import NCLS
from pathlib import Path
from tqdm.auto import tqdm
from datetime import datetime
from functools import reduce
from bs4 import BeautifulSoup
from typing import Tuple, List, Optional


def process_time(date_list: List) -> Tuple:
	# Convert start date.
	start_date = datetime.strptime(
		'-'.join(
			[date_list[0].lower()[:3], date_list[1]]),
		u'%b-%Y'
	).date()
	# Assign "-1" if current place of work.
	if len(date_list) in [4, 6]:
		end_date = -1
	# Convert end date.
	elif len(date_list) == 5:
		end_date = datetime.strptime(
			'-'.join(
				[date_list[3].lower()[:3], date_list[4]]),
			u'%b-%Y'
		).date()
	# Raise error if items not found.
	else:
		print(date_list)
		raise ValueError("Invalid date format")
	return start_date, end_date


def count_months(string_period: str) -> int:
	# Extract month and year.
	search_month = re.compile('(\d+)\sмесяц')
	search_year = re.compile('(\d+)\s(?:лет|год)')
	month = search_month.findall(string_period)
	year = search_year.findall(string_period)
	# Convert to months.
	m = int(month[0]) if len(month) > 0 else 0
	y = int(year[0]) * 12 if len(year) > 0 else 0
	return y + m


def parse_resume(
		file: Path,
		user_id: int,
		name_process_func: Optional[object] = None,
) -> np.array:

	time_path = [
		'bloko-column',
		'bloko-column_xs-4',
		'bloko-column_s-2',
		'bloko-column_m-2',
		'bloko-column_l-2',
	]

	person = []

	with open(file, 'r', encoding="utf-8") as f:
		# Read file content.
		contents = f.read()
		# Parse html.
		soup = BeautifulSoup(contents, "html.parser")
		try:
			# Get experience info.
			resume_experience = soup.find(
				'div', attrs={'data-qa': 'resume-block-experience'})
			# Get work time periods.
			resume_times = resume_experience.find_all(
				'div', attrs={'class': ' '.join(time_path)})
			# Get job names.
			resume_jobs = resume_experience.find_all(
				'div', attrs={'data-qa': 'resume-block-experience-position'})
			# Get job descriptions.
			resume_desc = resume_experience.find_all(
				'div', attrs={'data-qa': 'resume-block-experience-description'})
			# Iterate over jobs.
			for i in range(len(resume_times)):
				job = [user_id, ]
				# Get total experience period.
				time_span = resume_times[i].find_next('div').text
				# Finding tag whose child to be deleted.
				div_ = resume_times[i].find('div')
				# Delete the child element.
				div_.clear()
				# Create jod row.
				job.append(count_months(time_span))
				try:
					# Set localization.
					locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
					print('ru', resume_times[i].text.split())
					for d in process_time(resume_times[i].text.split()):
						job.append(d)
				except ValueError:
					pass
					# Set localization.
					locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
					print('ru', resume_times[i].text.split())
					for d in process_time(resume_times[i].text.split()):
						job.append(d)
				if name_process_func:
					job.append(name_process_func(resume_jobs[i].text))
				else:
					job.append(resume_jobs[i].text)
				job.append(resume_desc[i].text)
				person.append(job)
		except Exception as e:
			print(f"File {file.name} not parsed\n")
			print(e)
			pass
	print()
	print(person)
	return np.array(person)


def hh_job_preparation(string):
	"""функция обработки названий работ из резюме"""
	result = string.lower()
	temp_string = result
	result = result.replace("зам. ", "заместитель ")
	result = result.replace("нач. ", "начальник ")
	result = result.replace("рук. ", "руководитель ")
	result = result.replace("ген. ", "генеральный ")
	result = result.replace("гендиректор", "генеральный директор")
	result = result.replace("–", "-")
	result = result.replace(" - ", "-")

	if (result.find("(")>0 and result.find(")")>0):
		temp = ""
		not_closed = False
		for i in range(len(result)):
			if result[i] == "(":
				not_closed = True
			elif result[i] == ")":
				not_closed = False
			else:
				if not not_closed:
					temp += result[i]
		result = temp

	if (result.find("«")>0 and result.find("»")>0):
		temp = ""
		not_closed = False
		for i in range(len(result)):
			if result[i] == "«":
				not_closed = True
			elif result[i] == "»":
				not_closed = False
			else:
				if not not_closed:
					temp += result[i]
		result = temp
	if (result.find(",") > 0) :
		result=result.partition(',')[0]
	if (result.find(";") > 0) :
		result=result.partition(';')[0]
	if (result.find(".") > 0) :
		result=result.partition('.')[0]
	if (result.find("/") > 0) :
		result=result.partition('/')[0]
	if (result.find(" по ") > 0) :
		result=result.partition(' по ')[0]
	if (result.find("начальник ") > -1 or result.find("руководитель ") > -1):
		if (result.find("отдела") > -1):
			result = "начальник отдела"
		elif (result.find("службы") > -1):
			result = "начальник службы"
		elif (result.find("управления") > -1):
			result = "начальник управления"
		elif (result.find("подразделения") > -1):
			result = "начальник подразделения"
		elif (result.find("группы") > -1):
			result = "начальник группы"
	if (result.find("заместитель начальника") > -1 or result.find("заместитель руководителя ") > -1):
		if (result.find("отдела") > -1):
			result = "заместитель начальника отдела"
		elif (result.find("службы") > -1):
			result = "заместитель начальника службы"
		elif (result.find("управления") > -1):
			result = "заместитель начальника управления"
		elif (result.find("подразделения") > -1):
			result = "заместитель начальника подразделения"
		elif (result.find("группы") > -1):
			result = "заместитель начальника группы"
	if (result.find("developer") > -1 or result.find("programmer") > -1 ):
		result="программист"
	if (result.find("генеральный директор") > -1 or result.find("programmer") > -1 ):
		result="генеральный директор"
	result=result.strip()
	return(result)


def get_job_rank(df: pd.DataFrame) -> pd.DataFrame:

	list_of_dataframes = []

	df_ = df.assign(
		end_date_filled=lambda x: x['end_date'].replace(
			-1, datetime.now().date().replace(day=1)
		)
	)

	for i in tqdm(df.user_id.unique(), 'Processing users'):
		with warnings.catch_warnings():
			# Ignore pandas warnings.
			warnings.filterwarnings("ignore")
			# Select user data.
			temp = df_[df_['user_id'] == i]
			# Rank jobs by start and end dates.
			temp['job_level_simple'] = temp[
				["start_date", "end_date_filled"]
			].apply(tuple, axis=1).rank(method='dense').astype(int)
			# Find intersections between job periods to get dense rank.
			start = temp.start_date.apply(lambda x: int(x.strftime("%Y%m"))).values
			end = temp.end_date_filled.apply(lambda x: int(x.strftime("%Y%m"))).values
			idx = temp.index.values
			# Using ncls package algorithm.
			ncls = NCLS(start, end, idx)
			# Check overlappings.
			res = []
			for i in list(zip(start, end, idx)):
				ovlp = ncls.find_overlap(i[0], i[1])
				for j in ovlp:
					res.append({i: j})
			# Create aux columns.
			temp['copy_start_date'] = temp.loc[:, 'start_date']
			temp['copy_end_date'] = temp.loc[:, 'end_date_filled']
			# Reassign dates of ovelapping periods to obtain dense rank.
			exclude = []
			for i in res:
				(k, v), = i.items()
				if (k != v) & (k not in exclude):
					exclude.extend([k, v])
					srt = sorted([k, v])
					temp.loc[
						temp.index == srt[-1][2], 'copy_start_date'
					] = temp.loc[temp.index == srt[0][2]]['start_date'].values[0]
					temp.loc[
						temp.index == srt[-1][2], 'copy_end_date'
					] = temp.loc[temp.index == srt[0][2]]['end_date_filled'].values[0]
			# Get dense rank after reassignment.
			temp['job_level_intersect'] = temp[
				["copy_start_date", "copy_end_date"]
			].apply(tuple, axis=1).rank(method='dense').astype(int)
			# Delete aus columns.
			temp = temp.drop(columns=['end_date_filled', 'copy_start_date', 'copy_end_date'])
			# Add user data to the list of dataframes with all users.
			list_of_dataframes.append(temp)
	# Concatenate all data together.
	return reduce(lambda x, y: pd.concat([x, y]), list_of_dataframes)
